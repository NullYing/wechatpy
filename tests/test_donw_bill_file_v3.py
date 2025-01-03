# -*- coding: utf-8 -*-
import hashlib
import json
import os
import unittest
import pytest
from httmock import urlmatch, response, HTTMock

from wechatpy.pay.v3 import WeChatPay

_TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
_CERTS_PATH = os.path.join(_TESTS_PATH, "certs")
_FIXTURE_PATH = os.path.join(_TESTS_PATH, "fixtures", "pay/v3/")


@urlmatch(netloc=r"(.*\.)?api\.mch\.weixin\.qq\.com$")
def wechat_api_mock(url, request):
    path = (url.path[1:] if url.path.startswith("/") else url.path).replace("v3/", "").replace("/", "_")
    res_file = os.path.join(_FIXTURE_PATH, f"{path}.json")
    content = {
        "errcode": 99999,
        "errmsg": f"can not find fixture {res_file}",
    }
    headers = {"Content-Type": "application/json", "Wechatpay-Serial": "12345"}
    try:
        with open(res_file, "rb") as f:
            content = json.loads(f.read().decode("utf-8"))
    except (IOError, ValueError):
        pass
    return response(200, content, headers, request=request)

class DownBillFileTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WeChatPay(
            appid="abc1234",
            apiv3_key="test123",
            mch_id="1192221",
            wechat_cert_dir=_CERTS_PATH,
            apiclient_cert_path=os.path.join(_CERTS_PATH, "apiclient_cert.pem"),
            apiclient_key_path=os.path.join(_CERTS_PATH, "apiclient_key.pem"),
            skip_check_signature=True,  # 测试无法校验证书
        )

    def test_media(self):
        with HTTMock(wechat_api_mock):
            response = self.client.ecommerce.trade_bill("2024-12-31")
            print(response)