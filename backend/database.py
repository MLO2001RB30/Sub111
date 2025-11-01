import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "subtrack.db")

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize SQLite database with tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create subscriptions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                renewal_date TEXT NOT NULL,
                category TEXT DEFAULT 'Ukategoriseret',
                logo_url TEXT,
                currency TEXT DEFAULT 'DKK',
                transaction_date TEXT,
                owner_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("✅ Database initialized successfully")

async def get_user_by_email(email: str):
    """Get user by email"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

async def create_user(email: str, hashed_password: str):
    """Create a new user"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row)

async def create_subscription(data: dict):
    """Create a new subscription"""
    print("[create_subscription] Data being saved to SQLite:", data)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO subscriptions
            (title, amount, renewal_date, category, logo_url, currency, transaction_date, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("title"),
                data.get("amount"),
                data.get("renewal_date"),
                data.get("category", "Ukategoriseret"),
                data.get("logo_url"),
                data.get("currency", "DKK"),
                data.get("transaction_date"),
                data.get("owner_id")
            )
        )
        conn.commit()
        sub_id = cursor.lastrowid

        cursor.execute("SELECT * FROM subscriptions WHERE id = ?", (sub_id,))
        row = cursor.fetchone()
        result = dict(row)
        result['id'] = str(result['id'])
        return result

async def get_subscriptions_by_owner(owner_id: int):
    """Get all subscriptions for a specific owner"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM subscriptions WHERE owner_id = ? ORDER BY created_at DESC",
            (owner_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

async def delete_subscription(subscription_id: int):
    """Delete a subscription by ID"""
    print(f"[delete_subscription] Deleting subscription with ID: {subscription_id}")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE id = ?", (subscription_id,))
        conn.commit()
        print(f"[delete_subscription] Successfully deleted subscription {subscription_id}")
        return True
