#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试认证模块的验证码功能
"""

import asyncio
import sys
sys.path.append('.')

from src.auth import (
    SendCodeRequest,
    PhoneLoginRequest,
    generate_verification_code,
    store_verification_code,
    is_code_valid,
    init_db
)


async def test_verification_code():
    """测试验证码功能"""
    print("=== 测试验证码功能 ===")
    
    # 初始化数据库
    await init_db()
    print("✓ 数据库初始化完成")
    
    # 测试生成验证码
    code = generate_verification_code()
    print(f"✓ 生成验证码: {code}")
    assert len(code) == 6 and code.isdigit(), "验证码格式错误"
    
    # 测试存储和验证验证码
    phone = "13800138000"
    store_verification_code(phone, code)
    print(f"✓ 存储验证码: {phone} -> {code}")
    
    # 测试验证码验证
    assert is_code_valid(phone, code), "验证码验证失败"
    print("✓ 验证码验证成功")
    
    # 测试错误验证码
    assert not is_code_valid(phone, "000000"), "错误验证码应该验证失败"
    print("✓ 错误验证码正确拒绝")
    
    # 测试不存在的手机号
    assert not is_code_valid("13900139000", code), "不存在的手机号应该验证失败"
    print("✓ 不存在的手机号正确拒绝")
    
    print("\n=== 所有测试通过! ===")


if __name__ == "__main__":
    asyncio.run(test_verification_code())