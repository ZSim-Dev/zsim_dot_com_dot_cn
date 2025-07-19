from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .auth import (
    EmailLoginRequest,
    SendCodeRequest,
    UserCreate,
    get_current_user,
    login_user,
    login_with_email,
    register_user,
    send_verification_code,
)
from .auth import (
    close_db as close_auth_db,
)
from .auth import (
    init_db as init_auth_db,
)
from .github.release_api import LatestReleaseCache, get_latest_release_from_cache
from .vote import init_vote_db
from .vote import router as vote_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_databases()
    yield
    await close_auth_db()


app = FastAPI(lifespan=lifespan)

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


@app.post("/api/login-email")
async def login_email(request: EmailLoginRequest):
    """邮箱验证码登录"""
    return await login_with_email(request)


@app.get("/api/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}


@app.get("/api/github/latest-release")
async def get_latest_release() -> LatestReleaseCache:
    return await get_latest_release_from_cache()


@app.get("/api/is_in_release")
async def is_in_release() -> bool:
    return False
