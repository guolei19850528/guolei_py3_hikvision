#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import base64
import hashlib
import hmac
import uuid
from datetime import datetime
from typing import Union, Iterable, Callable

import requests
from addict import Dict
from guolei_py3_requests import RequestsResponseCallable, requests_request
from requests import Response


class RequestsResponseCallable(RequestsResponseCallable):
    @staticmethod
    def status_code_200_json_addict_code_0(response: Response = None):
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.code == 0 or json_addict.code == "0"

    @staticmethod
    def status_code_200_json_addict_code_0_data(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_code_0(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).data
        return Dict({})


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

    def signature(self, s: str = ""):
        return base64.b64encode(
            hmac.new(
                self.sk.encode(),
                s.encode(),
                digestmod=hashlib.sha256
            ).digest()
        ).decode()

    def get_requests_request_headers(
            self,
            method: str = "POST",
            path: str = "",
            requests_request_headers: dict = {}
    ):
        requests_request_headers = Dict(requests_request_headers)
        requests_request_headers = Dict({
            "accept": "*/*",
            "content-type": "application/json",
            "x-ca-signature-headers": "x-ca-key,x-ca-nonce,x-ca-timestamp",
            "x-ca-key": self.ak,
            "x-ca-nonce": self.nonce(),
            "x-ca-timestamp": str(self.timestamp()),
            **requests_request_headers,
        })
        s = "\n".join([
            method,
            requests_request_headers["accept"],
            requests_request_headers["content-type"],
            f"x-ca-key:{requests_request_headers['x-ca-key']}",
            f"x-ca-nonce:{requests_request_headers['x-ca-nonce']}",
            f"x-ca-timestamp:{requests_request_headers['x-ca-timestamp']}",
            path,
        ])
        requests_request_headers["x-ca-signature"] = self.signature(s=s)
        return requests_request_headers

    def requests_request_with_json(
            self,
            path: str = "",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """

        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1
        """
        if not isinstance(path, str):
            raise TypeError("path must be type string")
        if not len(path):
            raise ValueError("path must be type string and not empty")
        if not path.startswith("/artemis"):
            path = f"/artemis/{path[1:] if path.startswith('/') else path}"
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_headers = self.get_requests_request_headers(
            method="POST",
            path=path,
            requests_request_headers=requests_request_kwargs.headers
        )
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_kwargs_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
