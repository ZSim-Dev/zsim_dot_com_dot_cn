import json
import logging
from typing import List

import tomllib
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_credentials.models import Config
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

ACCESS_KEY_ID = config["aliyun"]["access_key_id"]
ACCESS_KEY_SECRET = config["aliyun"]["access_key_secret"]
SIGN_NAME = config["aliyun"]["sign_name"]
TEMPLATE_CODE = config["aliyun"]["template_code"]


class AliyunSMS:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        ak_config = Config(
            type="access_key",
            access_key_id=ACCESS_KEY_ID,
            access_key_secret=ACCESS_KEY_SECRET,
        )
        credential = CredentialClient(ak_config)
        config = open_api_models.Config(credential=credential)
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = "dysmsapi.aliyuncs.com"
        return Dysmsapi20170525Client(config)

    @staticmethod
    async def send_sms_async(
        args: List[str],
    ) -> None:
        """发送短信（通用方法）"""
        client = AliyunSMS.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers="your_value", sign_name="your_value"
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_sms_with_options_async(
                send_sms_request, util_models.RuntimeOptions()
            )
        except Exception as error:
            logging.error(error)
            raise

    @staticmethod
    async def send_verification_code(phone: str, code: str) -> None:
        """发送验证码短信

        Args:
            phone: 手机号
            code: 验证码

        Raises:
            Exception: 发送失败时抛出异常
        """
        client = AliyunSMS.create_client()

        # 构建模板参数
        template_param = json.dumps({"code": code})

        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=SIGN_NAME,
            template_code=TEMPLATE_CODE,
            template_param=template_param,
        )

        try:
            response = await client.send_sms_with_options_async(
                send_sms_request, util_models.RuntimeOptions()
            )

            # 检查发送结果
            if response.body.code != "OK":
                raise Exception(f"短信发送失败: {response.body.message}")

            logging.info(f"验证码发送成功，手机号: {phone}")

        except Exception as error:
            logging.error(f"验证码发送失败，手机号: {phone}, 错误: {error}")
            raise
