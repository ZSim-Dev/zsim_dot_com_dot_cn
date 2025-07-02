import hashlib
import os
import secrets
import time

import aiosqlite
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

DB_PATH = "./.database/users.db"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
fake_tokens: dict[str, str] = {}
# 验证码存储 {phone: {code: str, expire_time: float, last_send_time: float}}
verification_codes: dict[str, dict[str, str | float]] = {}


class UserCreate(BaseModel):
    """用户注册模型"""

    username: str = Field(
        ...,
        description="用户名",
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    password: str = Field(
        ...,
        description="密码",
        min_length=6,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    confirm_password: str = Field(
        ...,
        description="确认密码",
        min_length=6,
        max_length=20,
    )
    phone: str = Field(
        ...,
        description="手机号",
        min_length=11,
        max_length=11,
        pattern=r"^1[3-9]\d{9}$",
    )
    code: str = Field(
        ...,
        description="验证码",
        min_length=6,
        max_length=6,
    )


class PhoneLoginRequest(BaseModel):
    """手机号登录请求模型"""

    phone: str = Field(..., description="手机号")
    code: str = Field(..., description="验证码")


class SendCodeRequest(BaseModel):
    """发送验证码请求模型"""

    phone: str = Field(
        ...,
        description="手机号",
        pattern=r"^1[3-9]\d{9}$",
        min_length=11,
        max_length=11,
    )


async def init_db():
    """初始化数据库"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, phone TEXT UNIQUE)"
        )
        await conn.commit()


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_verification_code() -> str:
    """生成6位数字验证码"""
    return f"{secrets.randbelow(1000000):06d}"


def is_code_valid(phone: str, code: str) -> bool:
    """验证验证码是否有效"""
    if phone not in verification_codes:
        return False

    stored_data = verification_codes[phone]
    stored_code = stored_data.get("code")
    expire_time = stored_data.get("expire_time")

    if not stored_code or not expire_time:
        return False

    # 检查是否过期（5分钟有效期）
    if time.time() > expire_time:
        del verification_codes[phone]
        return False

    return stored_code == code


def store_verification_code(phone: str, code: str) -> None:
    """存储验证码"""
    current_time = time.time()
    verification_codes[phone] = {
        "code": code,
        "expire_time": current_time + 300,  # 5分钟有效期
        "last_send_time": current_time,  # 记录发送时间
    }


async def register_user(user: UserCreate) -> dict[str, str]:
    """用户注册"""
    # 验证密码确认
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="密码和确认密码不匹配")

    # 验证验证码
    if not is_code_valid(user.phone, user.code):
        raise HTTPException(status_code=401, detail="验证码无效或已过期")

    # 清除已使用的验证码
    if user.phone in verification_codes:
        del verification_codes[user.phone]

    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        try:
            await conn.execute(
                "INSERT INTO users (username, password, phone) VALUES (?, ?, ?)",
                (user.username, hash_password(user.password), user.phone),
            )
            await conn.commit()
        except aiosqlite.IntegrityError as e:
            error_msg = str(e)
            if "username" in error_msg:
                raise HTTPException(status_code=400, detail="用户名已存在")
            elif "phone" in error_msg:
                raise HTTPException(status_code=400, detail="手机号已被注册")
            else:
                raise HTTPException(
                    status_code=400, detail="注册失败，用户名或手机号已存在"
                )
    return {"msg": "注册成功"}


async def login_user(form_data: OAuth2PasswordRequestForm):
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
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


async def send_verification_code(request: SendCodeRequest) -> dict[str, str]:
    """发送验证码"""
    from .aliyun_sms import AliyunSMS

    current_time = time.time()

    # 检查发送频率限制（每分钟只能发送一次）
    if request.phone in verification_codes:
        last_send_time = verification_codes[request.phone].get("last_send_time", 0)
        if current_time - last_send_time < 60:  # 60秒内不能重复发送
            remaining_time = int(60 - (current_time - last_send_time))
            raise HTTPException(
                status_code=429,
                detail=f"发送过于频繁，请等待 {remaining_time} 秒后再试",
            )

    # 生成验证码
    code = generate_verification_code()
    print(f"[Auth]为手机号 {request.phone} 生成验证码: {code}")

    # 存储验证码
    store_verification_code(request.phone, code)

    try:
        # 发送短信
        await AliyunSMS.send_verification_code(request.phone, code)
        return {"msg": "验证码发送成功"}
    except Exception as e:
        # 发送失败时清除存储的验证码
        if request.phone in verification_codes:
            del verification_codes[request.phone]
        raise HTTPException(status_code=500, detail=f"验证码发送失败: {str(e)}")


async def login_with_phone(request: PhoneLoginRequest) -> dict[str, str]:
    """手机号验证码登录"""
    # 验证验证码
    if not is_code_valid(request.phone, request.code):
        raise HTTPException(status_code=401, detail="验证码无效或已过期")

    # 清除已使用的验证码
    if request.phone in verification_codes:
        del verification_codes[request.phone]

    # 检查用户是否存在
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT * FROM users WHERE phone=?", (request.phone,)
        ) as cur:
            user = await cur.fetchone()

    if not user:
        # 如果用户不存在，自动创建用户
        async with aiosqlite.connect(DB_PATH) as conn:
            try:
                await conn.execute(
                    "INSERT INTO users (username, password, phone) VALUES (?, ?, ?)",
                    (request.phone, "", request.phone),  # 用手机号作为用户名，密码为空
                )
                await conn.commit()
            except aiosqlite.IntegrityError:
                raise HTTPException(status_code=400, detail="用户创建失败")

    # 生成token
    token = secrets.token_hex(16)
    fake_tokens[token] = request.phone
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = fake_tokens.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="无效token")
    return username
