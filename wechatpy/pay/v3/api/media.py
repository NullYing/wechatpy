# -*- coding: utf-8 -*-
import hashlib
import json

from wechatpy.pay.v3.api.base import BaseWeChatPayAPI


class WeChatMedia(BaseWeChatPayAPI):
    def upload_image(self, file_bytes, filename, mimetype="image/jpg"):
        """
        上传图片

        :param file_bytes: 上传的文件二进制
        :param filename: 文件名
        :param mimetype: 文件mime type
        :return: 返回的结果数据
        """
        meta = {"filename": filename, "sha256": hashlib.sha256(file_bytes).hexdigest()}
        data = {
            "meta": json.dumps(meta),
        }
        return self._post(
            "merchant/media/upload", files=[("file", (filename, file_bytes, mimetype))], data=data, sign_data=meta
        )

    def cancel_applications_upload_image(self, file_bytes, file_name, mimetype="image/jpeg"):
        """
        图片上传
        电商平台服务商调用注销申请接口时，需要先调用本接口上传相关的资料图片，获取图片ID后，再填写到注销申请请求中。
        :param file_bytes: 上传的文件二进制
        :param file_name: 文件名
        :param mimetype: 文件mime type
        :return: 返回的结果数据
        """
        meta = {"file_name": file_name, "file_digest": hashlib.sha256(file_bytes).hexdigest()}
        data = {
            "meta": json.dumps(meta),
        }
        return self._post(
            "ecommerce/account/cancel-applications/media",
            files=[("file", (file_name, file_bytes, mimetype))], data=data, sign_data=meta,
            headers={"Content-Type": "multipart/form-data"}
        )
