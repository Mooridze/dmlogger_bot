import sqlite3

DB_NAME = "message.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    
    CREATE TABLE IF NOT EXISTS messages (
        chat_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        sender_id INTEGER,
        sender_username TEXT,
        sender_name TEXT,
        text TEXT,
        date TEXT,
        PRIMARY KEY (chat_id, message_id)
    )
    """)

    conn.commit()
    conn.close()

def save_message(chat_id, message_id, sender_id, sender_username, sender_name, text, date):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT OR REPLACE INTO messages (chat_id, message_id, sender_id, sender_username, sender_name, text, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, message_id, sender_id, sender_username, sender_name, text, date))
    conn.commit()
    conn.close()

def get_message(chat_id, message_id):
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("""
        SELECT text FROM messages WHERE chat_id = ? AND message_id = ?
    """, (chat_id, message_id))
    message = cursor.fetchone()
    conn.close()
    
    if message:
        return message[0]
    return None

def get_message_data(chat_id, message_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("""
        SELECT sender_username, sender_name, text FROM messages WHERE chat_id = ? AND message_id = ?
    """, (chat_id, message_id))
    message_data = cursor.fetchone()
    conn.close()

    return message_data

def update_message(chat_id, message_id, new_text):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        UPDATE messages SET text = ? WHERE chat_id = ? AND message_id = ?
    """, (new_text, chat_id, message_id))
    conn.commit()
    conn.close()