import json
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import pymysql
from dotenv import load_dotenv
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

load_dotenv()
'''
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)
MYSQL_USER = os.environ.get("MYSQL_USER", 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.environ.get("MYSQL_DB", 'samochody')

def connect():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
'''
db_config = {
    'host' : 'my-db',
    'user' : 'root',
    'password' : 'mypass123',
    'database' : 'samochody'
}
'''
@app.get("/name")
async def get_name():
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT `User` From `user`"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(json.dumps(rows))
    conn.close()
    return {"table_data": json.dumps(rows)}
'''


def get_all_samochody():
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT * FROM marki"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


@app.get("/samochody")
def get_all_samochody_endpoint(request, Request):
    all_samochody = get_all_samochody()
    return templates.TemplateResponse("all_samochody.html", {"request": request, "data": all_samochody})