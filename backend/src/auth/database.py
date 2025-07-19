import os
import time
import tomllib

import aiosqlite

with open("backend/config.toml", "rb") as f:
    config = tomllib.load(f)
    DB_PATH = config["database"]["auth_db_path"]


class AuthDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def connect(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self._create_tables()

    async def close(self):
        await self.conn.close()

    async def _create_tables(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT UNIQUE
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                email TEXT PRIMARY KEY,
                code TEXT,
                expire_time REAL
            )
        """)
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                username TEXT,
                expire_time REAL
            )
        """)
        await self.conn.commit()

    # User management
    async def create_user(self, username, password_hash, email):
        try:
            await self.conn.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password_hash, email)
            )
            await self.conn.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

    async def get_user_by_username(self, username):
        cursor = await self.conn.execute("SELECT * FROM users WHERE username=?", (username,))
        return await cursor.fetchone()

    async def get_user_by_email(self, email):
        cursor = await self.conn.execute("SELECT * FROM users WHERE email=?", (email,))
        return await cursor.fetchone()

    # Verification code management
    async def store_code(self, email, code, expire_duration=300):
        expire_time = time.time() + expire_duration
        await self.conn.execute(
            "REPLACE INTO verification_codes (email, code, expire_time) VALUES (?, ?, ?)", (email, code, expire_time)
        )
        await self.conn.commit()

    async def get_code(self, email):
        cursor = await self.conn.execute("SELECT * FROM verification_codes WHERE email=?", (email,))
        return await cursor.fetchone()

    async def delete_code(self, email):
        await self.conn.execute("DELETE FROM verification_codes WHERE email=?", (email,))
        await self.conn.commit()

    # Token management
    async def store_token(self, token, username, expire_duration=86400):  # 24 hours
        expire_time = time.time() + expire_duration
        await self.conn.execute(
            "REPLACE INTO tokens (token, username, expire_time) VALUES (?, ?, ?)", (token, username, expire_time)
        )
        await self.conn.commit()

    async def get_username_by_token(self, token):
        cursor = await self.conn.execute("SELECT * FROM tokens WHERE token=?", (token,))
        token_data = await cursor.fetchone()
        if token_data and time.time() < token_data["expire_time"]:
            return token_data["username"]
        return None

    async def delete_expired_tokens(self):
        await self.conn.execute("DELETE FROM tokens WHERE expire_time < ?", (time.time(),))
        await self.conn.commit()
