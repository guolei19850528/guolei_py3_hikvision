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

    def api_resource_v1_vehicle_batch_add(
            self,
            path: str = "/artemis/api/resource/v1/vehicle/batch/add",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量添加车辆

        单个添加车辆信息接口，注意，车辆的必选字段必须都包括在入参中。

        若需支持批量添加的后续业务处理，请求需指定每个车辆的clientId，服务端完成添加后将生成的车辆indexCode与此clientId绑定返回，服务端不对clientId做校验。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#bb06a569
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

    def api_resource_v1_vehicle_single_update(
            self,
            path: str = "/artemis/api/resource/v1/vehicle/single/update",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        修改车辆

        根据车辆编号修改车辆信息。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#c805b274
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

    def api_resource_v1_vehicle_batch_delete(
            self,
            path: str = "/artemis/api/resource/v1/vehicle/batch/delete",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        批量删除车辆

        根据车辆编码删除车辆。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#b250bd27
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

    def api_resource_v2_vehicle_advance_vehicleList(
            self,
            path: str = "/artemis/api/resource/v2/vehicle/advance/vehicleList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆列表v2

        查询车辆列表接口可以根据车牌号码、车主姓名、车辆类型、车牌类型、是否关联人员、车辆状态这些查询条件来进行高级查询；若不指定查询条件，即全量获取所有的车辆信息。返回结果分页展示。

        注：若指定多个查询条件，表示将这些查询条件进行“与”的组合后进行精确查询

        当一个车辆属于多个区域时，查询时会返回多条记录。

        当返回字段对应的值为空时，该字段不返回。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#d3f8970f
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

    def api_resource_v1_park_parkList(
            self,
            path: str = "/artemis/api/resource/v1/park/parkList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取停车库列表

        根据停车场唯一标识集合获取停车库列表信息。

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#d93e4991
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

    def api_resource_v1_park_search(
            self,
            path: str = "/artemis/api/resource/v1/park/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询停车库节点信息

        查询停车库节点信息，支持同时查询多种类型的节点，用于异步展示停车、搜索等场景。

        示例：
        当parentIndexCode、parentResourceType传”123”，” parking”,时，resourceTypes传parking时返回停车库”123”下面的子库信息；

        当parentIndexCode、parentResourceType传”123”，” parking”,时，resourceTypes传entrance时，返回停车库”123”下面的出入口；

        当parentIndexCode、parentResourceType传”123”，” parking”,时，resourceTypes传parkFloor时，返回停车库”123”下面的楼层信息；

        当parentIndexCode、parentResourceType传”123”，” parking”,时，resourceTypes传parking 、entrance、parkFloor时，同时返回停车库”123”下面的子库、出入口、楼层；

        当parentIndexCode、parentResourceType传”456”，” entrance”,时，resourceTypes传rodaway返回出入口”456”下面的车道。

        当返回字段对应的值为空时，该字段不返回。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#c8512008
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

    def api_resource_v1_park_detail_get(
            self,
            path: str = "/artemis/api/resource/v1/park/detail/get",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取停车库节点详细信息

        根据节点编号indexCode、类型查询节点详细信息。

        当返回字段对应的值为空时，该字段不返回。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#bdc1e803
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

    def api_resource_v1_entrance_entranceList(
            self,
            path: str = "/artemis/api/resource/v1/entrance/entranceList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取出入口列表

        根据节点编号indexCode、类型查询节点详细信息。

        根据停车场唯一标识集合取指定的车入口信息

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#e7828411
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

    def api_resource_v1_roadway_roadwayList(
            self,
            path: str = "/artemis/api/resource/v1/roadway/roadwayList",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        获取车道列表

        根据出入口唯一标识集合获取车道信息

        综合安防管理平台iSecure Center V1.0及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E8%BD%A6%E8%BE%86%E5%8F%8A%E8%BD%A6%E5%BA%93%E4%BF%A1%E6%81%AF#cb0db770
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

    def api_pms_v1_tempCarInRecords_page(
            self,
            path: str = "/artemis/api/pms/v1/tempCarInRecords/page",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询场内车停车信息

        简述：场内车停车信息即为某一停车库或部分停车库内未出场车辆的信息，包括车牌号、车辆入场时间、车辆图片等，是用于停车场缴费、场内找车等业务的前置业务场景。

        支持：支持通过停车库的唯一标识、车牌号码（模糊）、停车时长及停车库信息查询场内车停车信息。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#c4292e21
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

    def api_pms_v1_car_charge(
            self,
            path: str = "/artemis/api/pms/v1/car/charge",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        车辆充值

        简述：车辆添加后，有临时车、固定车之分，充值包期后是固定车，未包期或包期过期的是临时车，车辆出场需要进行收费。

        支持：支持通过车牌号进行特定停车场的包期充值。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bc8e5872
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

    def api_pms_v1_car_charge_deletion(
            self,
            path: str = "/artemis/api/pms/v1/car/charge/deletion",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        取消车辆包期

        简述：车辆取消包期后变为临时车，可以取消某个停车库的包期，也可以取消平台所有停车库下的包期。

        支持：支持通过车牌号、停车库编号取消包期；停车库编号可为空，为空时取消平台所有包期。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#d95589de
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

    def api_pms_v1_car_charge_page(
            self,
            path: str = "/artemis/api/pms/v1/car/charge/page",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询车辆包期信息

        简述：车辆包期后在当前停车场是固定车，自由进出场；在未包期的停车场进出场是临时车，需要收费。可通过此接口查询平台所有车辆或某个停车场里车辆的包期状态，便于展示车辆包期状态和是否固定车查询。

        支持：支持通过车牌号、停车场编号分页查询车辆包期信息。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E8%BD%A6%E8%BE%86%E7%AE%A1%E6%8E%A7-%E5%81%9C%E8%BD%A6%E5%9C%BA%E5%8A%9F%E8%83%BD#bb7cb58c
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

    def api_acps_v1_authDownload_special_person_diy(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/special/person/diy",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        按人员详情与设备下发

        针对少量权限（100设备通道*1000人）的下发场景，以异步任务方式下发出入控制权限。

        1、接口支持下发优先级设置。优先级分为正常与快速两种方式，默认优先级为正常，其他异步下发接口的优先级都为正常方式。高优先级方式下发适用于需要权限快速生效的场景，但是频繁的使用高优先方式会造成下发队列的频繁切换可能会造成下发性能下降，请根据业务场景选择。

        2、在当前任务中设置回调地址，每当一个设备下发完成时，通过回调地址主动通知调用方，采用restful回调模式，支持http和https，样式如下：http://ip:port/downloadRcv或者 https://ip:port/downloadRcv，建议业务组件在设置回调地址接收时，异步处理内部逻辑，避免请求超时（5秒超时）

        3、 当添加系统外人员时，如果系统外人员中涉及数据（指纹、人脸模型数据）、卡密码敏感信息的需要通过《秘钥交换》接口后加密传输。

        4、 每个tagId全局默认最多保持1000个可操作（未下发结束）任务列表。

        说明：调用方在使用该接口下发权限时，如果也使用权限配置功能，那么可能会造成人员权限冲突的情况，acps以最后一次操作数据为准；比如对人员配置了权限又通过该接口删除权限，通过配置和指定下发分别下发不同的计划模板等。

        发布版本：V1.5.0

        综合安防管理平台iSecure Center V1.5及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#ffc16d00
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

    def api_acps_v1_authDownload_special_person_diy_result(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/special/person/diy/result",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        按人员详情与设备下发

        根据人员或设备通道分页查询人员详情与设备下发信息。

        发布版本：V1.5.0

        综合安防管理平台iSecure Center V1.5及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#c23a646b
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

    def api_acps_v1_authDownload_task_addition(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/addition",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        创建下载任务_根据人员与设备通道指定下载

        创建下载任务，以异步任务方式下载出入控制权限。适用于综合大楼、学校、医院等批量权限下载的场景。

        创建下载任务，使得业务组件与出入控制权限服务建立一次异步下载的通道。

        通过向下载任务中添加数据接口添加待下载的数据，包含资源、人员信息；可分多次调用该接口批量添加下载数据。

        任务的操作权限由创建的业务组件控制，包含开始下载任务，终止下载任务，删除下载任务。

        对已经开始的下载任务，可通过查询下载任务进度接口查询任务的总体下载进度和每个资源的下载进度信息。

        一个下载任务最大支持100个设备的卡权限下载或者100个通道的人脸。

        新创建的下载任务有效期7天，在7天内未操作开始下载的任务将自动清理。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#eb5ccf35
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

    def api_acps_v1_authDownload_data_addition(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/data/addition",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        下载任务中添加数据_根据人员与设备通道指定下载

        该接口支持向新建的下载任务中添加待下载的权限数据，可通过本接口分多次向下载任务中添加数据。

        单次接口最多支持100个设备资源和1000个人员，可分多次添加，多次添加的数据会合并处理。

        同一个资源相同的人员重复添加时，以最后一次为准。

        该接口强依赖于资源目录公共存储，请确保设备与人员相关的信息已存在公共存储，否则下载必定失败。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#c8be1732
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

    def api_acps_v1_authDownload_task_simpleDownload(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/simpleDownload",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        简单同步权限下载_根据人员与设备通道指定下载

        简单权限下载主要用途对单个指定设备通道，下载少量简单的需即时生效的权限。通过同步下载方式下载权限，适合公安出租屋等场景。

        使用该接口时无需创建下载任务，权限下载记录同步返回，接口超时时间30秒。

        权限类型为人脸时，设备通道对象中的通道号有且只有一个。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#b95f0c75
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

    def api_acps_v1_authDownload_task_start(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/start",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        开始下载任务

        该接口用于开始一次下载任务，只能由创建任务的组件触发。权限下载完成后会自动结束下载任务。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#b969dda3
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

    def api_acps_v1_authDownload_task_progress(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/progress",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询下载任务进度

        根据任务ID查询任务的下载进度，只能查询由组件创建的任务，进度信息包含任务总体下载进度及各个资源的下载进度。

        建议该接口调用频率每3-5秒查询一次任务的下载进度。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#fd3de11f
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

    def api_acps_v1_authDownload_task_list(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/list",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询正在下载的任务列表

        该接口用于查询正在下载的任务编号列表，只能查询由组件创建的任务.

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#a0904bf7
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

    def api_acps_v1_authDownload_task_deletion(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/deletion",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        删除未开始的下载任务

        该接口用于删除创建的下载任务，已经开始下载的任务不能删除，只能由创建任务的组件触发。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#b6f7ff3b
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

    def api_acps_v1_authDownload_task_stop(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/stop",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        终止正在下载的任务

        该接口用于终止正在下载的任务，未开始下载的任务不能停止，只能由创建任务的组件触发。当全部资源已终止下载后会自动结束下载任已经终止下载的任务，将会被清除出任务列表，无法被再次开启。

        终止下载任务时丢弃还未下载的数据，对已下载的数据记录下载记录和日志。

        综合安防管理平台iSecure Center V1.2及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#a6347f19
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

    def api_acps_v1_authDownload_task_search(
            self,
            path: str = "/artemis/api/acps/v1/authDownload/task/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询任务信息列表

        该接口用于分页查询任务的详细信息

        综合安防管理平台iSecure Center V1.5及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#e2363b12
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

    def api_acps_v1_download_record_channel_list_search(
            self,
            path: str = "/artemis/api/acps/v1/download_record/channel/list/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询设备通道权限下载记录列表

        根据查询条件分页查询设备通道的下载记录，只能查询由业务组件自身创建的任务下载记录。

        下载记录主要展示此次下载的概览信息，可通过查询设备通道的下载记录详情接口查询每个设备通道中人员的下载详情。

        支持通过任务编号查询单个任务的下载记录。

        支持通过设备通道查询设备通道的历史下载记录（卡权限下载记录只能通过设备查询，人脸下载可通过设备和通道查询）。

        支持通过任务编号、设备通道对象、下载时间、下载类型查询历史下载记录。

        该接口仅返回分页的列表数据，不返回总数。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#faa5eb84
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

    def api_acps_v1_download_record_channel_total_search(
            self,
            path: str = "/artemis/api/acps/v1/download_record/channel/total/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询设备通道权限下载记录总数

        根据查询条件查询设备通道的下载记录总数。

        综合安防管理平台iSecure Center V1.3及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#f9f581ee
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

    def api_acps_v2_download_record_person_detail_search(
            self,
            path: str = "/artemis/api/acps/v2/download_record/person/detail/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询设备通道的人员权限下载详情v2

        根据查询条件查询设备通道的人员下载详情。

        该接口用于查询单个下载任务某一设备通道的下载详情信息。

        接口仅返回分页的列表数据，不返回总数。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#dad1a642
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

    def api_acps_v2_download_record_person_total_search(
            self,
            path: str = "/artemis/api/acps/v2/download_record/person/total/search",
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_code_0_data,
            requests_request_args: Iterable = tuple(),
            requests_request_kwargs: dict = {},
    ):
        """
        查询设备通道的人员权限下载详情总数v2

        根据查询条件查询设备通道的人员下载详情总数，支持下载中和已完成下载的设备通道查询。

        综合安防管理平台iSecure Center V1.4及以上版本

        @see https://open.hikvision.com/docs/docId?productId=5c67f1e2f05948198c909700&version=%2Ff95e951cefc54578b523d1738f65f0a1&tagPath=API%E5%88%97%E8%A1%A8-%E4%B8%80%E5%8D%A1%E9%80%9A%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1-%E4%B8%80%E5%8D%A1%E9%80%9A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86#c6c53587
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
