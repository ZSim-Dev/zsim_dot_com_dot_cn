import asyncio

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import (
    UserCreate,
    get_current_user,
    init_db,
    login_user,
    register_user,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

asyncio.run(init_db())


@app.post("/api/register")
async def register(user: UserCreate):
    return await register_user(user)


@app.post("/api/login")
async def login(form_data=Depends()):
    return await login_user(form_data)


@app.get("/api/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}
