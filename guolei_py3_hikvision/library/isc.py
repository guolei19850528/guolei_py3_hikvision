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
from typing import Callable, Any

from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallable(ResponseCallable):
    """
    Response Callable Class
    """

    @staticmethod
    def json_addict__code_is_0___data(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallable.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "code": {
                    "status": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ],
                },
            },
            "required": ["code", "data"]
        }).is_valid(json_addict):
            return json_addict.data
        return Dict()


class UrlsSetting:
    pass


class Api(object):
    def __init__(
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
            headers: dict = {}
    ):
        headers = Dict(headers) if isinstance(headers, Dict) else Dict()
        headers = Dict({
            "accept": "*/*",
            "content-type": "application/json",
            "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
            "x-ca-key": self.ak,
            "x-ca-nonce": self.nonce(),
            "x-ca-timestamp": str(self.timestamp()),
        })
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
        return headers.to_dict()

    def post(
            self,
            response_callable: Callable = ResponseCallable.json_addict__code_is_0___data,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        headers = self.headers(method="POST", path=url, headers=headers)
        return self.request(
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            verify=False,
            **kwargs
        )

    def request(
            self,
            response_callable: Callable = ResponseCallable.json_addict__code_is_0___data,
            method: str = "GET",
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.host}{url}"
        print(url)
        return request(
            response_callable=response_callable,
            method=method,
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )
