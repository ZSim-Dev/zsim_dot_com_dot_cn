import hashlib
import secrets
import time

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from .database import AuthDatabase
from .email import send_email

db = AuthDatabase()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class UserCreate(BaseModel):
    """用户注册模型"""

    username: str = Field(..., description="用户名", min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., description="密码", min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    confirm_password: str = Field(..., description="确认密码", min_length=6, max_length=20)
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., description="验证码", min_length=6, max_length=6)


class EmailLoginRequest(BaseModel):
    """邮箱登录请求模型"""

    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., description="验证码")


class SendCodeRequest(BaseModel):
    """发送验证码请求模型"""

    email: EmailStr = Field(..., description="邮箱地址")
    purpose: str = Field("login", description="用途: login 或 register")


async def init_db():
    """初始化数据库"""
    await db.connect()
    await db.delete_expired_tokens()


async def close_db():
    """关闭数据库"""
    await db.close()


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_verification_code() -> str:
    """生成6位数字验证码"""
    return f"{secrets.randbelow(1000000):06d}"


async def is_code_valid(email: str, code: str) -> bool:
    """验证验证码是否有效"""
    stored_data = await db.get_code(email)
    if not stored_data:
        return False

    if time.time() > stored_data["expire_time"]:
        await db.delete_code(email)
        return False

    return stored_data["code"] == code


async def register_user(user: UserCreate) -> dict[str, str]:
    """用户注册"""
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="密码和确认密码不匹配")

    if not await is_code_valid(user.email, user.code):
        raise HTTPException(status_code=401, detail="验证码无效或已过期")

    await db.delete_code(user.email)

    password_hash = hash_password(user.password)
    success = await db.create_user(user.username, password_hash, user.email)

    if not success:
        user_by_email = await db.get_user_by_email(user.email)
        if user_by_email:
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        raise HTTPException(status_code=400, detail="用户名已存在")

    return {"msg": "注册成功"}


async def login_user(form_data: OAuth2PasswordRequestForm):
    user = await db.get_user_by_username(form_data.username)
    if not user or user["password"] != hash_password(form_data.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = secrets.token_hex(16)
    await db.store_token(token, user["username"])
    return {"access_token": token, "token_type": "bearer"}


async def send_verification_code(request: SendCodeRequest) -> dict[str, str]:
    """发送验证码"""
    user_exists = await db.get_user_by_email(request.email)

    if request.purpose == "register" and user_exists:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    elif request.purpose == "login" and not user_exists:
        raise HTTPException(status_code=400, detail="该邮箱未注册")

    code_data = await db.get_code(request.email)
    if code_data and time.time() < code_data["expire_time"] - 240:  # 60秒内不能重复发送
        remaining_time = int(code_data["expire_time"] - time.time() - 240)
        raise HTTPException(status_code=429, detail=f"发送过于频繁，请等待 {remaining_time} 秒后再试")

    code = generate_verification_code()
    await db.store_code(request.email, code)

    print(f"[Auth]为邮箱 {request.email} 生成验证码: {code}")

    try:
        subject = "ZSim验证码"
        content = (
            f"<h1>ZSim</h1><div>您的验证码是: {code}，请在5分钟内使用。</div><div>如果非本人操作，请忽略此邮件。</div>"
        )
        send_email(request.email, subject, content)
        return {"msg": "验证码发送成功"}
    except Exception as e:
        await db.delete_code(request.email)
        raise HTTPException(status_code=500, detail=f"验证码发送失败: {str(e)}")


async def login_with_email(request: EmailLoginRequest) -> dict[str, str]:
    """邮箱验证码登录"""
    if not await is_code_valid(request.email, request.code):
        raise HTTPException(status_code=401, detail="验证码无效或已过期")

    await db.delete_code(request.email)

    user = await db.get_user_by_email(request.email)
    if not user:
        # 如果用户不存在，自动创建用户
        password_hash = hash_password(secrets.token_hex(16))  # Generate a random password
        await db.create_user(request.email, password_hash, request.email)
        user = await db.get_user_by_email(request.email)

    if not user:
        raise HTTPException(status_code=500, detail="创建用户后无法检索")

    token = secrets.token_hex(16)
    await db.store_token(token, user["username"])
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = await db.get_username_by_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="无效token")
    return username
