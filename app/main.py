from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.environ.get('MYSQL_DB', 'projekt')

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_db = {
    "root": {
        "username": "root",
        "full_name": "admin",
        "hashed_password": "$2b$12$iC1IqX5xmoMPMuNbKPFr8.GRBU4eyFyo16PWhleUDsFk3ZT82RCIe",
        "disabled": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    full_name: str or None = None
    disabled: bool or None = None

class Film(BaseModel):
    nazwa: str
    gatunek: str
    rok: int

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

def connect():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

def create_film(nazwa, gatunek, rok):
    conn=connect()
    cursor=conn.cursor()
    query = "INSERT INTO filmy (nazwa, gatunek, rok) VALUES (%s,%s,%s)"
    values = (nazwa, gatunek, rok)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return cursor.lastrowid

def delete_film(film_id: int):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM filmy WHERE id = %s", (film_id,))
    film = cursor.fetchone()
    if film:
        cursor.execute("DELETE FROM filmy WHERE id = %s", (film_id,))
        conn.commit()
        conn.close()
        return {"message": "Film usunięty"}
    else:
        raise HTTPException(status_code=404, detail="Brak takiego filmu")

def update_film(film_id: int, film_update: Film):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM filmy WHERE id = %s", (film_id,))
    film = cursor.fetchone()
    if film:
        cursor.execute("UPDATE filmy SET nazwa=%s, gatunek=%s, rok=%s WHERE id=%s",
                (film_update.nazwa, film_update.gatunek, film_update.rok, film_id))
        conn.commit()
        conn.close()
        return {"message": "Film zaktualizowany"}
    else:
        raise HTTPException(status_code=404, detail="Brak takiego filmu")

def create_film(new_film: Film):
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM filmy WHERE nazwa = %s", (new_film.nazwa,))
    film = cursor.fetchone()
    if film:
        raise HTTPException(status_code=400, detail="Film juz istnieje")
    else:
        cursor.execute("INSERT INTO filmy (nazwa, gatunek, rok) VALUES (%s, %s, %s)",
                (new_film.nazwa, new_film.gatunek, new_film.rok))
        conn.commit()
        conn.close()
        return {"message": "Film dodany"}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credential_exception
    
    user = get_user(fake_db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.get("/all")
async def wszystkie_filmy():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("SELECT id, nazwa, gatunek, rok FROM filmy")
    myresult = cursor.fetchall()
    conn.close()
    return {"message": myresult}

@app.post("/filmy")
async def create_film_endpoint(new_film: Film, current_user: User = Depends(get_current_active_user)):
    return create_film(new_film)
    
@app.delete("/filmy/{film_id}")
async def delete_film_id(film_id: int, current_user: User = Depends(get_current_active_user)):
    return delete_film(film_id)

@app.put("/filmy/{film_id}")
async def update_film_id(film_id: int, film_update:Film, current_user: User = Depends(get_current_active_user)):
    return update_film(film_id, film_update)

