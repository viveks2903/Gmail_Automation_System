import sqlite3

def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id TEXT PRIMARY KEY,
        sender TEXT,
        recipient TEXT,
        subject TEXT,
        received_at TEXT,
        snippet TEXT,
        is_read BOOLEAN DEFAULT FALSE
    )
    """)



def insert_email(cursor, email_data):
    cursor.execute("""
    INSERT INTO emails (id, sender, recipient, subject, received_at, snippet, is_read)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, email_data)
    

def get_unread_emails(cursor):
    cursor.execute("SELECT * FROM emails WHERE is_read = 0")
    return cursor.fetchall()

print("✅ Database and table created successfully.")

