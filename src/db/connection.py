import dotenv
import psycopg2
import os

dotenv.load_dotenv()  # Load environment variables from .env file

DB_NAME = os.getenv("POSTGRES_DB") or os.getenv("DB_NAME")
DB_USER = os.getenv("POSTGRES_USER") or os.getenv("DB_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD") or os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST") or os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT") or os.getenv("DB_PORT", "5432")

DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


if __name__ == "__main__":
    # Test the connection
    conn  = create_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("PostgreSQL version:", version)
        conn.close()