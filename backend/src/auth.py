import hashlib
import os
import secrets

import aiosqlite
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

DB_PATH = "./.database/users.db"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
fake_tokens = {}


class UserCreate(BaseModel):
    username: str
    password: str


async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
        )
        await conn.commit()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


async def register_user(user: UserCreate):
    async with aiosqlite.connect(DB_PATH) as conn:
        try:
            await conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, hash_password(user.password)),
            )
            await conn.commit()
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=400, detail="用户名已存在")
    return {"msg": "注册成功"}


async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (form_data.username, hash_password(form_data.password)),
        ) as cur:
            user = await cur.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = secrets.token_hex(16)
    fake_tokens[token] = user["username"]
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = fake_tokens.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="无效token")
    return username
