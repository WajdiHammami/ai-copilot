import dotenv
import psycopg2
import os




if __name__ == "__main__":
    dotenv.load_dotenv()  # Load environment variables from .env file


    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cur = conn.cursor()

    # Execute SQL from sql file
    with open("data/sql/create_schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    try:
        commands = sql.split(';')
        for command in commands:
            command = command.strip()
            if command:
                cur.execute(command)
        conn.commit()
        print("Database schema reset successfully.")
    except Exception as e:
        print("Error resetting database schema:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()