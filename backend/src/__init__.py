import hashlib
import os
import secrets
import sqlite3

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# 添加CORS中间件，允许前端跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "./.database/users.db"


def get_db():
    # 如果数据库文件不存在，则先初始化数据库
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
    )
    conn.commit()
    conn.close()


# 启动时初始化数据库
init_db()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserCreate(BaseModel):
    username: str
    password: str


@app.post("/api/register")
def register(user: UserCreate):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hash_password(user.password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="用户名已存在")
    finally:
        conn.close()
    return {"msg": "注册成功"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# 简单token存储（生产环境请用JWT）
fake_tokens = {}


@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    cur = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (form_data.username, hash_password(form_data.password)),
    )
    user = cur.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    # 生成token
    token = secrets.token_hex(16)
    fake_tokens[token] = user["username"]
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = fake_tokens.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="无效token")
    return username


@app.get("/api/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}
