#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_hikvision
=================================================
"""
import base64
import hashlib
import hmac
import uuid
from datetime import datetime
from typing import Callable

import requests
from jsonschema.validators import Draft202012Validator
from requests import Response


class UrlSetting(object):
    pass


class ResponseCallable(object):
    """
    Response Callable Class
    """

    @staticmethod
    def json_code_0_data(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "code": {
                    "oneOf": [
                        {"type": "string", "const": "0"},
                        {"type": "integer", "const": 0},
                    ]
                },
            },
            "required": ["code", "data"]
        }).is_valid(json_data):
            return json_data.get("data", dict())
        return None


class Api(object):
    def _init_(
            self,
            host: str = "",
            ak: str = "",
            sk: str = "",
    ):
        self._host = host
        self._ak = ak
        self._sk = sk

    @property
    def host(self):
        return self._host[:-1] if self._host.endswith("/") else self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def ak(self):
        return self._ak

    @ak.setter
    def ak(self, value):
        self._ak = value

    @property
    def sk(self):
        return self._sk

    @sk.setter
    def sk(self, value):
        self._sk = value

    def timestamp(self):
        return int(datetime.now().timestamp() * 1000)

    def nonce(self):
        return uuid.uuid4().hex

    def signature(self, string: str = ""):
        return base64.b64encode(
            hmac.new(
                self.sk.encode(),
                string.encode(),
                digestmod=hashlib.sha256
            ).digest()
        ).decode()

    def headers(
            self,
            method: str = "POST",
            path: str = "",
            headers: dict = dict()
    ):
        headers = headers or dict()
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
            "x-ca-key": self.ak,
            "x-ca-nonce": self.nonce(),
            "x-ca-timestamp": str(self.timestamp()),
            **headers
        }
        string = "\n".join([
            method,
            headers["accept"],
            headers["content-type"],
            f"x-ca-key:{headers['x-ca-key']}",
            f"x-ca-nonce:{headers['x-ca-nonce']}",
            f"x-ca-timestamp:{headers['x-ca-timestamp']}",
            path,
        ])
        headers["x-ca-signature"] = self.signature(string=string)
        return headers

    def get(self, on_response_callback: Callable = ResponseCallable.json_code_0_data, path: str = None,
            **kwargs):
        """
        execute get by requests.get

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.host}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.host}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.get(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post(self, on_response_callback: Callable = ResponseCallable.json_code_0_data, path: str = None,
             **kwargs):
        """
        execute post by requests.post

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.host}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.host}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def put(self, on_response_callback: Callable = ResponseCallable.json_code_0_data, path: str = None,
            **kwargs):
        """
        execute put by requests.put

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.host}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.host}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.put(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = ResponseCallable.json_code_0_data, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.host}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.host}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.request(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post_json(self, on_response_callback: Callable = ResponseCallable.json_code_0_data, path: str = None,
                  **kwargs):
        """
        execute post by requests.post

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.host}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        kwargs.setdefault("verify", False)
        kwargs.setdefault("timeout", (120, 120))
        headers = kwargs.get("headers", dict())
        headers = self.headers(method="POST", path=path, headers=headers)
        path = kwargs.get("url", None) or f"{self.host}{path}"
        kwargs.update([
            ("headers", headers),
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response
