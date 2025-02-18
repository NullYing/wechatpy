import hashlib
import json
import os
import unittest
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


class WeChatPayTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WeChatPay(
            appid="11",
            apiv3_key="",
            mch_id="11",
            wechat_cert_dir=_CERTS_PATH,
            apiclient_cert_path=os.path.join(_CERTS_PATH, "apiclient_cert.pem"),
            apiclient_key_path=os.path.join(_CERTS_PATH, "apiclient_key.pem"),
            skip_check_signature=True,  # 测试无法校验证书
        )

    def test_media(self):
        with HTTMock(wechat_api_mock):
            data = b""
            sha256_data = hashlib.sha256(data).hexdigest()
            response = self.client.media.cancel_applications_upload_image(data, "test.jpeg", sha256_data)
            self.assertIn("media_id", response)

    def test_cancel_applications(self):
        with HTTMock(wechat_api_mock):
            application_info = [{"application_type": "SP_MERCHANT_APPLICATION",
                                 "application_media_id": "abc123456"}]
            body_response = self.client.ecommerce.cancel_applications(123456789, 123456789, application_info)
            assert_body_response = {
                "out_apply_no": "abcd12345FEGH",
                "sub_mchid": "123456789",
                "reject_reason": "非电商服务商，无权调用此接口",
                "cancel_state": "REVIEWING",
                "update_time": "2023-01-20T13:29:35+08:00"
            }
            self.assertEqual(body_response, assert_body_response)
