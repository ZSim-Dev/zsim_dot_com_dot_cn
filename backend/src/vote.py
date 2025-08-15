import json
import os
import tomllib
from io import StringIO

import aiosqlite
import httpx
import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from .auth import get_current_user

router = APIRouter()

with open("backend/config.toml", "rb") as f:
    config = tomllib.load(f)
    DB_PATH = config["database"]["vote_db_path"]
AVATARS_PATH = os.path.join(os.path.dirname(__file__), "assets", "avatars.json")

# Load characters data into memory on startup
try:
    with open(AVATARS_PATH, "r", encoding="utf-8") as f:
        CHARACTERS_DATA: list[dict] = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    CHARACTERS_DATA = []

# Load character details from GitHub CSV
CHARACTER_DETAILS: list[dict] = []


async def fetch_character_details():
    """从GitHub获取并解析角色详细数据CSV文件"""
    global CHARACTER_DETAILS
    csv_url = "https://raw.githubusercontent.com/LoTwT/ZSim/refs/heads/main/zsim/data/character.csv"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(csv_url)
            response.raise_for_status()

            # 使用 Polars 解析CSV内容
            df = pl.read_csv(StringIO(response.text))

            # 添加角色支持度计算
            df_with_support = df.with_columns(
                pl.when((pl.col("动作建模") >= 1) & (pl.col("Buff支持") >= 1) & (pl.col("影画支持") >= 1))
                .then(pl.lit(1))
                .when((pl.col("动作建模") >= 0) & (pl.col("Buff支持") >= 0))
                .then(pl.lit(0))
                .otherwise(pl.lit(-1))
                .alias("角色支持度")
            )

            CHARACTER_DETAILS = df_with_support.to_dicts()

    except Exception as e:
        print(f"Error fetching character details: {e}")
        CHARACTER_DETAILS = []


async def init_vote_db():
    """初始化投票数据库和表"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as conn:
        # 存储每个角色的票数
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS character_votes (
                character_id INTEGER PRIMARY KEY,
                votes INTEGER NOT NULL DEFAULT 0
            )"""
        )
        # 存储用户的投票记录，防止重复投票
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS user_votes (
                username TEXT NOT NULL,
                character_id INTEGER NOT NULL,
                PRIMARY KEY (username, character_id)
            )"""
        )
        await conn.commit()

    # 初始化角色详细数据
    await fetch_character_details()


@router.get("/vote/user_votes", tags=["Vote"])
async def get_user_votes(current_user: str = Depends(get_current_user)):
    """获取当前用户的投票记录"""
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT character_id FROM user_votes WHERE username = ?", (current_user,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


@router.get("/vote/characters", tags=["Vote"])
async def get_characters_with_votes():
    """获取所有角色及其票数"""
    if not CHARACTERS_DATA:
        raise HTTPException(status_code=500, detail="角色数据文件未找到或加载失败")

    """获取所有角色详细数据"""
    if not CHARACTER_DETAILS:
        # 如果数据为空，尝试重新获取
        await fetch_character_details()

    if not CHARACTER_DETAILS:
        raise HTTPException(status_code=500, detail="角色详细数据获取失败")

    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT * FROM character_votes") as cursor:
            votes_rows = await cursor.fetchall()
            votes_map = {row["character_id"]: row["votes"] for row in votes_rows}

    characters_with_votes = CHARACTERS_DATA[:]

    # 创建角色详细数据的映射，使用CID作为键
    character_details_map = {}
    for detail in CHARACTER_DETAILS:
        cid = detail.get("CID")
        if cid is not None:
            character_details_map[cid] = detail

    for char in characters_with_votes:
        char["votes"] = votes_map.get(char["id"], 0)
        char["icon_url"] = char["icon"][0] if char.get("icon") else ""

    result = []
    for char in characters_with_votes:
        # 从 CHARACTER_DETAILS 中获取额外信息，使用CID匹配
        detail = character_details_map.get(char["id"])

        """
        # 映射规则
        # 将支持度数值转换为图标
        def map_support_to_icon(value: float | int) -> str:
        if value >= 1:
            return "✅ 完全"
        elif value <= -1:
            return "❌ 不支持"
        else:
            return "⚠️ 不完全"
        """
        char_result = {
            "id": char["id"],
            "name": char["name"],
            "name_en": char["name_en"],
            "avatar": char["icon_url"],
            "votes": char["votes"],
            "action_modeling": detail.get("动作建模", "") if detail else "",
            "buff_support": detail.get("Buff支持", "") if detail else "",
            "cinema_support": detail.get("影画支持", "") if detail else "",
            "frame_counting": detail.get("精细测帧", "") if detail else "",
            "character_support": detail.get("角色支持度", "") if detail else "",
        }
        result.append(char_result)

    return result


@router.post("/vote/character/{character_id}", tags=["Vote"])
async def vote_for_character(character_id: int, current_user: str = Depends(get_current_user)):
    """为指定角色投票"""
    async with aiosqlite.connect(DB_PATH) as conn:
        # 检查用户是否已投票
        async with conn.execute(
            "SELECT 1 FROM user_votes WHERE username = ? AND character_id = ?",
            (current_user, character_id),
        ) as cursor:
            if await cursor.fetchone():
                raise HTTPException(status_code=400, detail="您已经投过票了")

        # 开启事务
        async with conn.execute("BEGIN") as cursor:
            try:
                # 增加角色票数
                await conn.execute(
                    "INSERT INTO character_votes (character_id, votes) VALUES (?, 1) ON CONFLICT(character_id) DO UPDATE SET votes = votes + 1",
                    (character_id,),
                )
                # 记录用户投票
                await conn.execute(
                    "INSERT INTO user_votes (username, character_id) VALUES (?, ?)",
                    (current_user, character_id),
                )
                await conn.commit()
            except aiosqlite.Error as e:
                await conn.rollback()
                raise HTTPException(status_code=500, detail=f"数据库操作失败: {e}")

    return {"msg": "投票成功"}
