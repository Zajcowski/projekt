import json
from fastapi import FastAPI
import pymysql
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)
MYSQL_USER = os.environ.get("MYSQL_USER", 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.environ.get("MYSQL_DB", 'mysql')

def connect():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

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