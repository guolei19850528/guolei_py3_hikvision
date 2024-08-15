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

    def requests_request_with_json_post(
            self,
            path: str = "",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        使用json请求接口

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1
        :param path: example /artemis/api/resource/v1/regions/root
        :param requests_request_kwargs_json: json data
        :param requests_response_callable: guolei_py3_requests.RequestsResponseCallable instance
        :param requests_request_args: guolei_py3_requests.requests_request(*requests_request_args, **requests_request_kwargs)
        :param requests_request_kwargs: guolei_py3_requests.requests_request(*requests_request_args, **requests_request_kwargs)
        :return:
        """
        if not isinstance(path, str):
            raise TypeError("path must be type string")
        if not len(path):
            raise ValueError("path must be type string and not empty")
        path = f"/{path}" if not path.startswith('/') else path
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

    def api_resource_v1_org_rootOrg(
            self,
            path: str = "/artemis/api/resource/v1/org/rootOrg",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取根组织

        获取根组织接口用来获取组织的根节点。

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#b83c9200
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_org_orgList(
            self,
            path: str = "/artemis/api/resource/v1/org/orgList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取组织列表

        根据该接口全量同步组织信息,不作权限过滤，返回结果分页展示。

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#b8da83b5
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_org_advance_orgList(
            self,
            path: str = "/artemis/api/resource/v2/org/advance/orgList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询组织列表v2

        根据不同的组织属性分页查询组织信息。

        查询组织列表接口可以根据组织唯一标识集、组织名称、组织状态等查询条件来进行高级查询。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#eea0304a
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_org_parentOrgIndexCode_subOrgList(
            self,
            path: str = "/artemis/api/resource/v1/org/parentOrgIndexCode/subOrgList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据父组织编号获取下级组织列表

        根据父组织编号获取下级组织列表，主要用于逐层获取父组织的下级组织信息，返回结果分页展示。

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E7%BB%84%E7%BB%87%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#bc702d7d
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_org_timeRange(
            self,
            path: str = "/artemis/api/resource/v1/org/timeRange",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        增量获取组织数据

        根据查询条件查询组织列表信息，主要根据时间段分页获取组织数据，包含已删除数据。其中开始日期与结束日期的时间差必须在1-48小时内。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#e1ed492e
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_org_orgIndexCodes_orgInfo(
            self,
            path: str = "/artemis/api/resource/v1/org/orgIndexCodes/orgInfo",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据组织编号获取组织详细信息

        根据组织编号orgIndexCode列表获取指定的组织信息，如存在多组织则返回总条数及多组织信息。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E5%8C%BA%E5%9F%9F%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#deca25c2
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_resource_properties(
            self,
            path: str = "/artemis/api/resource/v1/resource/properties",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取资源属性

        查询当前平台指定资源已定义的属性信息集合， 适用于平台资源自定义属性的场景， 部分接口需要使用这部分自定义属性。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#de003a88
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_person_single_add(
            self,
            path: str = "/artemis/api/resource/v2/person/single/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        添加人员v2

        添加人员信息接口，注意，在安保基础数据配置的必选字段必须都包括在入参中。

        人员添加的时候，可以指定人员personId，不允许与其他人员personId重复，包括已删除的人员。

        本接口支持人员信息的扩展字段，按照属性定义key:value上传即可， 可通过获取资源属性接口，获取平台已启用的人员属性信息。

        综合安防管理平台iSecure Center V1.5及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#b6a07b38
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_single_add(
            self,
            path: str = "/artemis/api/resource/v1/person/single/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        添加人员v1

        添加人员信息接口，注意，在安保基础数据配置的必选字段必须都包括在入参中。

        人员添加的时候，可以指定人员personId，不允许与其他人员personId重复，包括已删除的人员。

        本接口支持人员信息的扩展字段，按照属性定义key:value上传即可， 可通过获取资源属性接口，获取平台已启用的人员属性信息。

        综合安防管理平台iSecure Center V1.5及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#b6a07b38
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_single_update(
            self,
            path: str = "/artemis/api/resource/v1/person/single/update",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改人员

        根据人员编号修改人员信息。

        本接口支持人员信息的扩展字段，按照属性定义key:value上传即可， 可通过获取资源属性接口，获取平台已启用的人员属性信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#a5a1036a
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_batch_add(
            self,
            path: str = "/artemis/api/resource/v1/person/batch/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加人员

        添加人员信息接口，注意，在安保基础数据配置的必选字段必须都包括在入参中。

        批量添加仅支持人员基础属性。

        人员批量添加的时候，可以指定人员personId，不允许与其他人员personId重复，包括已删除的人员。

        如果用户不想指定personId，那么需要指定clientId，请求内的每一条数据的clientid必须唯一， 返回值会将平台生成的personid与clientid做绑定。

        若personId和clientId都不指定，则无法准确判断哪部分人员添加成功。

        本接口支持人员信息的扩展字段，按照属性定义key:value上传即可， 可通过获取资源属性接口，获取平台已启用的人员属性信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#bf9b034d
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_batch_delete(
            self,
            path: str = "/artemis/api/resource/v1/person/batch/delete",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量删除人员

        根据编号删除人员，人员删除是软删除，被删除人员会出现在人员信息“已删除人员”页面中，支持批量删除人员。进入“已删除人员”页面再次删除将会同时删除人员关联的指纹和人脸信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#f2a13521
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_face_single_add(
            self,
            path: str = "/artemis/api/resource/v1/face/single/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        添加人脸

        添加人脸信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#ae3a260f
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_face_single_update(
            self,
            path: str = "/artemis/api/resource/v1/face/single/update",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改人脸

        根据人脸Id修改人脸。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#a38f12ec
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_face_single_delete(
            self,
            path: str = "/artemis/api/resource/v1/face/single/delete",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        删除人脸

        根据人脸Id删除人脸。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#dd554fad
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_person_orgIndexCode_personList(
            self,
            path: str = "/artemis/api/resource/v2/person/orgIndexCode/personList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取组织下人员列表v2

        根据组织编号获取组织下的人员信息列表，返回结果分页展示。

        本接口支持自定义属性的返回， 通过获取资源属性接口获取平台已支持人员属性的说明。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#c602940a
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_person_personList(
            self,
            path: str = "/artemis/api/resource/v2/person/personList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取人员列表v2

        获取人员列表接口可用来全量同步人员信息，返回结果分页展示。

        本接口支持自定义属性的返回， 通过获取资源属性接口获取平台已支持人员属性的说明。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#aa136eca
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v2_person_advance_personList(
            self,
            path: str = "/artemis/api/resource/v2/person/advance/personList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询人员列表v2

        查询人员列表接口可以根据人员ID集、人员姓名、人员性别、所属组织、证件类型、证件号码、人员状态这些查询条件来进行高级查询；若不指定查询条件，即全量获取所有的人员信息。返回结果分页展示。

        注：若指定多个查询条件，表示将这些查询条件进行”与”的组合后进行精确查询。

        根据”人员名称personName”查询为模糊查询。

        本接口支持自定义属性的返回，及自定义属性进行查找， 通过获取资源属性接口获取平台已支持人员属性的说明。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#dd9d9d0b
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_condition_personInfo(
            self,
            path: str = "/artemis/api/resource/v1/person/condition/personInfo",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据人员唯一字段获取人员详细信息

        获取人员信息接口，可以根据实名标识(证件号码、人员ID、手机号码、工号)来精确查询人员信息，并返回总数量。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#f2f0dee2
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_person_picture(
            self,
            path: str = "/artemis/api/resource/v1/person/picture",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        提取人员图片

        根据获取人员信息的接口中拿到的图片URI和图片服务器唯一标识，通过该接口得到完整的URL，可以直接从图片服务下载图；

        此接口返回重定向请求redirect：picUrl

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E4%BA%BA%E5%91%98%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3-%E4%BA%BA%E5%91%98%E5%8F%8A%E7%85%A7%E7%89%87%E6%8E%A5%E5%8F%A3#f2f0dee2
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v2_resource_resourcesByParams(
            self,
            path: str = "/artemis/api/irds/v2/resource/resourcesByParams",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询资源列表v2

        根据条件查询目录下有权限的资源列表。

        当返回字段对应的值为空时，该字段不返回。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E8%B5%84%E6%BA%90%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v2_resource_subResources(
            self,
            path: str = "/artemis/api/irds/v2/resource/subResources",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据区域获取下级资源列表v2

        根据区域编码、资源类型、资源操作权限码分页获取当前区域下（不包含子区域）有权限的资源列表，主要用于逐层获取区域下的资源信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E8%B5%84%E6%BA%90%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#af61c5f9
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_irds_v2_deviceResource_resources(
            self,
            path: str = "/artemis/api/irds/v2/deviceResource/resources",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取资源列表v2

        根据资源类型分页获取资源列表，主要用于资源信息的全量同步。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E8%B5%84%E6%BA%90%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#cbc52c56
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def api_resource_v1_resource_indexCodes_search(
            self,
            path: str = "/artemis/api/resource/v1/resource/indexCodes/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        根据编号查询资源详细信息

        根据资源类型、资源编号查询单个资源详细信息及总条数，列表中资源类型必须一致。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%B5%84%E6%BA%90%E7%9B%AE%E5%BD%95-%E8%B5%84%E6%BA%90%E4%BF%A1%E6%81%AF%E6%8E%A5%E5%8F%A3#d77ea3ed
        :param path:
        :param requests_request_kwargs_json:
        :param requests_response_callable:
        :param requests_request_args:
        :param requests_request_kwargs:
        :return:
        """
        return self.requests_request_with_json_post(
            path=path,
            requests_request_kwargs_json=requests_request_kwargs_json,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
