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

    def api_pms_v1_car_charge_page(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆包期信息

        简述：车辆包期后在当前停车场是固定车，自由进出场；在未包期的停车场进出场是临时车，需要收费。可通过此接口查询平台所有车辆或某个停车场里车辆的包期状态，便于展示车辆包期状态和是否固定车查询。

        支持：支持通过车牌号、停车场编号分页查询车辆包期信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bb7cb58c
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/pms/v1/car/charge/page"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v1_car_charge(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        车辆充值

        简述：车辆添加后，有临时车、固定车之分，充值包期后是固定车，未包期或包期过期的是临时车，车辆出场需要进行收费。

        支持：支持通过车牌号进行特定停车场的包期充值。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bc8e5872
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/pms/v1/car/charge"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v1_car_charge_deletion(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        取消车辆包期

        简述：车辆取消包期后变为临时车，可以取消某个停车库的包期，也可以取消平台所有停车库下的包期。

        支持：支持通过车牌号、停车库编号取消包期；停车库编号可为空，为空时取消平台所有包期。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#d95589de
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/pms/v1/car/charge/deletion"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v_1_tempCarInRecords_page(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询场内车停车信息

        简述：场内车停车信息即为某一停车库或部分停车库内未出场车辆的信息，包括车牌号、车辆入场时间、车辆图片等，是用于停车场缴费、场内找车等业务的前置业务场景。

        支持：支持通过停车库的唯一标识、车牌号码（模糊）、停车时长及停车库信息查询场内车停车信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#c4292e21
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/pms/v1/tempCarInRecords/page"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_vehicle_advance_vehicleList(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆列表v2

        查询车辆列表接口可以根据车牌号码、车主姓名、车辆类型、车牌类型、是否关联人员、车辆状态这些查询条件来进行高级查询；若不指定查询条件，即全量获取所有的车辆信息。返回结果分页展示。
        注：若指定多个查询条件，表示将这些查询条件进行“与”的组合后进行精确查询 当一个车辆属于多个区域时，查询时会返回多条记录。当返回字段对应的值为空时，该字段不返回。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#d3f8970f
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/resource/v2/vehicle/advance/vehicleList"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_batch_add(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加车辆

        单个添加车辆信息接口，注意，车辆的必选字段必须都包括在入参中。

        若需支持批量添加的后续业务处理，请求需指定每个车辆的clientId，服务端完成添加后将生成的车辆indexCode与此clientId绑定返回，服务端不对clientId做校验。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#bb06a569
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/resource/v1/vehicle/batch/add"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_single_update(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改车辆

        根据车辆编号修改车辆信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#c805b274
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/resource/v1/vehicle/single/update"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_batch_delete(
            self,
            requests_request_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量删除车辆

        根据车辆编码删除车辆。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#b250bd27
        :param requests_request_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """

        requests_request_json = Dict(requests_request_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        path = "/artemis/api/resource/v1/vehicle/batch/delete"
        requests_request_headers = self.get_requests_request_headers(method="POST", path=path,
                                                                     requests_request_headers=requests_request_kwargs.headers)
        requests_request_kwargs = Dict({
            "url": f"{self.host}{path}",
            "method": "POST",
            "verify": False,
            "headers": {
                **requests_request_headers,
            },
            "json": {
                **requests_request_json,
                **requests_request_kwargs.json,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
