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

    def _requests_request_with_json(
            self,
            path: str = "",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        if not isinstance(path, str):
            raise TypeError("path must be type string")
        if not len(path):
            raise ValueError("path must be type string and not empty")
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

    def api_pms_v1_car_charge_page(
            self,
            path="/artemis/api/pms/v1/car/charge/page",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆包期信息

        简述：车辆包期后在当前停车场是固定车，自由进出场；在未包期的停车场进出场是临时车，需要收费。可通过此接口查询平台所有车辆或某个停车场里车辆的包期状态，便于展示车辆包期状态和是否固定车查询。

        支持：支持通过车牌号、停车场编号分页查询车辆包期信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bb7cb58c
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v1_car_charge(
            self,
            path="/artemis/api/pms/v1/car/charge",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        车辆充值

        简述：车辆添加后，有临时车、固定车之分，充值包期后是固定车，未包期或包期过期的是临时车，车辆出场需要进行收费。

        支持：支持通过车牌号进行特定停车场的包期充值。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bc8e5872
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v1_car_charge_deletion(
            self,
            path="/artemis/api/pms/v1/car/charge/deletion",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        取消车辆包期

        简述：车辆取消包期后变为临时车，可以取消某个停车库的包期，也可以取消平台所有停车库下的包期。

        支持：支持通过车牌号、停车库编号取消包期；停车库编号可为空，为空时取消平台所有包期。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#d95589de
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_pms_v_1_tempCarInRecords_page(
            self,
            path="/artemis/api/pms/v1/tempCarInRecords/page",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询场内车停车信息

        简述：场内车停车信息即为某一停车库或部分停车库内未出场车辆的信息，包括车牌号、车辆入场时间、车辆图片等，是用于停车场缴费、场内找车等业务的前置业务场景。

        支持：支持通过停车库的唯一标识、车牌号码（模糊）、停车时长及停车库信息查询场内车停车信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#c4292e21
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_vehicle_advance_vehicleList(
            self,
            path="/artemis/api/resource/v2/vehicle/advance/vehicleList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆列表v2

        查询车辆列表接口可以根据车牌号码、车主姓名、车辆类型、车牌类型、是否关联人员、车辆状态这些查询条件来进行高级查询；若不指定查询条件，即全量获取所有的车辆信息。返回结果分页展示。
        注：若指定多个查询条件，表示将这些查询条件进行“与”的组合后进行精确查询 当一个车辆属于多个区域时，查询时会返回多条记录。当返回字段对应的值为空时，该字段不返回。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#d3f8970f
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_batch_add(
            self,
            path="/artemis/api/resource/v1/vehicle/batch/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加车辆

        单个添加车辆信息接口，注意，车辆的必选字段必须都包括在入参中。

        若需支持批量添加的后续业务处理，请求需指定每个车辆的clientId，服务端完成添加后将生成的车辆indexCode与此clientId绑定返回，服务端不对clientId做校验。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#bb06a569
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_single_update(
            self,
            path="/artemis/api/resource/v1/vehicle/single/update",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改车辆

        根据车辆编号修改车辆信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#c805b274
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_vehicle_batch_delete(
            self,
            path="/artemis/api/resource/v1/vehicle/batch/delete",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量删除车辆

        根据车辆编码删除车辆。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#b250bd27
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_regions_root(
            self,
            path="/artemis/api/resource/v1/regions/root",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取根区域信息

        获取根区域信息。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v2_region_nodesByParams(
            self,
            path="/artemis/api/irds/v2/region/nodesByParams",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询区域列表v2

        根据查询条件查询区域列表信息，主要用于区域信息查询过滤。

        相对V1接口，支持级联场景的区域查询。

        当返回字段对应的值为空时，该字段不返回。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_regions_subRegions(
            self,
            path="/artemis/api/resource/v2/regions/subRegions",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据区域编号获取下一级区域列表v2

        根据用户请求的资源类型和资源权限获取父区域的下级区域列表，主要用于逐层获取父区域的下级区域信息，例如监控点预览业务的区域树的逐层获取。下级区域只包括直接下级子区域

        。注：查询区域管理权限（resourceType为region），若父区域的子区域无权限、但是其孙区域有权限时，会返回该无权限的子区域，但是该区域的available标记为false（表示无权限）

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#cd531e45
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_regions(
            self,
            path="/artemis/api/resource/v1/regions",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        分页获取区域列表

        获取区域列表接口可用来全量同步区域信息，返回结果分页展示。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#d0c1cc14
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_region_regionCatalog_regionInfo(
            self,
            path="/artemis/api/resource/v1/region/regionCatalog/regionInfo",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据编号获取区域详细信息

        根据区域编号查询区域详细信息及总条数，主要用于区域详细信息展示。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#e8a9bcc2
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_region_timeRange(
            self,
            path="/artemis/api/resource/v1/region/timeRange",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        增量获取区域数据

        根据查询条件查询区域信息列表，主要根据时间段分页获取区域数据，包含已删除数据。其中开始日期与结束日期的时间差必须在1-48小时内。

        当返回字段对应的值为空时，该字段不返回。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#fe88e93c
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_region_batch_add(
            self,
            path="/artemis/api/resource/v1/region/batch/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加区域

        支持区域的批量添加。三方可以自行指定区域的唯一标识，也可以由ISC平台自行生成。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#e21ca7e1
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_region_batch_add(
            self,
            path="/artemis/api/resource/v1/region/batch/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加区域

        支持区域的批量添加。三方可以自行指定区域的唯一标识，也可以由ISC平台自行生成。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#e21ca7e1
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_region_single_update(
            self,
            path="/artemis/api/resource/v1/region/single/update",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改区域

        根据区域标志修改区域信息

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#e0ef8bd3
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v1_card_cardInfo(
            self,
            path="/artemis/api/irds/v1/card/cardInfo",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取单个卡片信息

        获取卡片列表接口可用来全量同步卡片信息，返回结果分页展示，不作权限过滤。
        注：卡号为精确查找

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8D%A1%E7%89%87%E6%8E%A5%E5%8F%A3#fb03b6d3
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v1_card_advance_cardList(
            self,
            path="/artemis/api/irds/v1/card/advance/cardList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询卡片列表

        查询卡片列表接口可以根据卡片号码、人员姓名、卡片状态、人员ID集合等查询条件来进行高级查询；若不指定查询条件，即全量获取所有的卡片信息。返回结果分页展示。
        注：若指定多个查询条件，表示将这些查询条件进行“与”的组合后进行查询。
        “人员名称personName”条件查询为模糊查询。
        “卡片号码cardNo”条件查询为模糊查询。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8D%A1%E7%89%87%E6%8E%A5%E5%8F%A3#f10c7c7e
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_card_timeRange(
            self,
            path="/artemis/api/resource/v1/card/timeRange",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        增量获取卡片数据

        根据查询条件查询卡片列表信息，主要根据时间段分页获取卡片信息，包含已删除数据。其中开始日期与结束日期的时间差必须在48小时内。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8D%A1%E7%89%87%E6%8E%A5%E5%8F%A3#d95a940b
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_cis_v1_card_bindings(
            self,
            path="/artemis/api/cis/v1/card/bindings",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量开卡

        该接口主要是应用于对多个人同时开卡的场景，输入卡片开始有效日期、卡片截止有效日期以及对应的人员、卡片关联列表，实现对多个人员同时开卡的功能，开卡成功后，可以到相应子系统开启卡片的权限，例如到门禁子系统开启人员门禁权限。

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8D%A1%E7%89%87%E6%8E%A5%E5%8F%A3#d75b749c
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self._requests_request_with_json(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
