import asyncio

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .auth import (
    PhoneLoginRequest,
    SendCodeRequest,
    UserCreate,
    get_current_user,
    init_db as init_auth_db,
    login_user,
    login_with_phone,
    register_user,
    send_verification_code,
)
from .vote import init_vote_db
from .vote import router as vote_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init_databases():
    await init_auth_db()
    await init_vote_db()


asyncio.run(init_databases())

app.include_router(vote_router, prefix="/api")


@app.post("/api/register")
async def register(user: UserCreate):
    return await register_user(user)


@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data)


@app.post("/api/send-code")
async def send_code(request: SendCodeRequest):
    """发送验证码"""
    return await send_verification_code(request)


@app.post("/api/login-phone")
async def login_phone(request: PhoneLoginRequest):
    """手机号验证码登录"""
    return await login_with_phone(request)


@app.get("/api/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}
