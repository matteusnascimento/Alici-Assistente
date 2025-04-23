import psycopg2
import os

def init_db():
    conn = psycopg2.connect(
        dbname="Mateus nascimento dos Santos",
        user="Mateus270320",
        password="Mateus270320",
        host="db.bit.io",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        sender_id TEXT,
        text TEXT,
        sender_type TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
