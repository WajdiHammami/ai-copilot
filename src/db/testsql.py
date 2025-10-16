from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()  # reads the .env file and populates os.environ

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    print("Connection successful:", conn.status)
    conn.close()
except Exception as e:
    print("Connection failed:", e)