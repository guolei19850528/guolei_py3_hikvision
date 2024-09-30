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


class UrlsSetting:
    API__RESOURCE__V1__REGIONS__ROOT = "/api/resource/v1/regions/root"
    API__IRDS__V2__REGION__NODESBYPARAMS = "/api/irds/v2/region/nodesByParams"
    API__RESOURCE__V2__REGIONS__SUBREGIONS = "/api/resource/v2/regions/subRegions"
    API__RESOURCE__V1__REGIONS = "/api/resource/v1/regions"
    API__RESOURCE__V1__REGION__REGIONCATALOG__REGIONINFO = "/api/resource/v1/region/regionCatalog/regionInfo"
    API__RESOURCE__V1__REGION__TIMERANGE = "/api/resource/v1/region/timeRange"
    API__RESOURCE__V1__REGION__BATCH__ADD = "/api/resource/v1/region/batch/add"
    API__RESOURCE__V1__REGION__SINGLE__UPDATE = "/api/resource/v1/region/single/update"
    API__CIS__V1__CARD__BINDINGS = "/api/cis/v1/card/bindings"
    API__CIS__V1__CARD__DELETION = "/api/cis/v1/card/deletion"
    API__CIS__V1__CARD__BATCH__LOSS = "/api/cis/v1/card/batch/loss"
    API__CIS__V1__CARD__BATCH__UNLOSS = "/api/cis/v1/card/batch/unLoss"
    API__CIS__V1__CARD__BARCODE = "/api/cis/v1/card/barCode"
    API__RESOURCE__V1__CARD__CARDLIST = "/api/resource/v1/card/cardList"
    API__IRDS__V1__CARD__CARDINFO = "/api/irds/v1/card/cardInfo"
    API__IRDS__V1__CARD__ADVANCE__CARDLIST = "/api/irds/v1/card/advance/cardList"
    API__RESOURCE__V1__CARD__TIMERANGE = "/api/resource/v1/card/timeRange"
    API__RESOURCE__V1__ORG__SINGLE__UPDATE = "/api/resource/v1/org/single/update"
    API__RESOURCE__V1__ORG__BATCH__DELETE = "/api/resource/v1/org/batch/delete"
    API__RESOURCE__V1__ORG__BATCH__ADD = "/api/resource/v1/org/batch/add"
    API__RESOURCE__V1__ORG__ROOTORG = "/api/resource/v1/org/rootOrg"
    API__RESOURCE__V1__ORG__ORGLIST = "/api/resource/v1/org/orgList"
    API__RESOURCE__V2__ORG__ADVANCE__ORGLIST = "/api/resource/v2/org/advance/orgList"
    API__RESOURCE__V1__ORG__PARENTORGINDEXCODE__SUBORGLIST = "/api/resource/v1/org/parentOrgIndexCode/subOrgList"
    API__RESOURCE__V1__ORG__TIMERANGE = "/api/resource/v1/org/timeRange"
    API__RESOURCE__V1__ORG__ORGINDEXCODES__ORGINFO = "/api/resource/v1/org/orgIndexCodes/orgInfo"
    API__RESOURCE__V1__RESOURCE__PROPERTIES = "/api/resource/v1/resource/properties"
    API__RESOURCE__V2__PERSON__SINGLE__ADD = "/api/resource/v2/person/single/add"
    API__RESOURCE__V1__PERSON__BATCH__ADD = "/api/resource/v1/person/batch/add"
    API__RESOURCE__V1__PERSON__SINGLE__UPDATE = "/api/resource/v1/person/single/update"
    API__RESOURCE__V1__PERSON__BATCH__DELETE = "/api/resource/v1/person/batch/delete"
    API__RESOURCE__V1__FACE__SINGLE__ADD = "/api/resource/v1/face/single/add"
    API__RESOURCE__V1__FACE__SINGLE__UPDATE = "/api/resource/v1/face/single/update"
    API__RESOURCE__V1__FACE__SINGLE__DELETE = "/api/resource/v1/face/single/delete"
    API__RESOURCE__V2__PERSON__ORGINDEXCODE__PERSONLIST = "/api/resource/v2/person/orgIndexCode/personList"
    API__RESOURCE__V2__PERSON__PERSONLIST = "/api/resource/v2/person/personList"
    API__RESOURCE__V2__PERSON__ADVANCE__PERSONLIST = "/api/resource/v2/person/advance/personList"
    API__RESOURCE__V1__PERSON__CONDITION__PERSONINFO = "/api/resource/v1/person/condition/personInfo"
    API__RESOURCE__V1__PERSON__PERSONLIST__TIMERANGE = "/api/resource/v1/person/personList/timeRange"
    API__RESOURCE__V1__PERSON__PICTURE = "/api/resource/v1/person/picture"
    API__IRDS__V2__RESOURCE__RESOURCESBYPARAMS = "/api/irds/v2/resource/resourcesByParams"
    API__IRDS__V2__RESOURCE__SUBRESOURCES = "/api/irds/v2/resource/subResources"
    API__IRDS__V2__DEVICERESOURCE__RESOURCES = "/api/irds/v2/deviceResource/resources"
    API__RESOURCE__V1__RESOURCE__TIMERANGE = "/api/resource/v1/resource/timeRange"
    API__RESOURCE__V1__RESOURCE__INDEXCODES__SEARCH = "/api/resource/v1/resource/indexCodes/search"
    API__NMS__V1__ONLINE__HISTORY_STATUS = "/api/nms/v1/online/history_status"
    API__RESOURCE__V2__ENCODEDEVICE__SEARCH = "/api/resource/v2/encodeDevice/search"
    API__RESOURCE__V1__ENCODEDEVICE__SUBRESOURCES = "/api/resource/v1/encodeDevice/subResources"
    API__RESOURCE__V1__ENCODEDEVICE__TIMERANGE = "/api/resource/v1/encodeDevice/timeRange"
    API__RESOURCE__V2__CAMERA__SEARCH = "/api/resource/v2/camera/search"
    API__RESOURCE__V1__CAMERAS = "/api/resource/v1/cameras"
    API__RESOURCE__V1__REGIONS__REGIONINDEXCODE__CAMERAS = "/api/resource/v1/regions/regionIndexCode/cameras"
    API__RESOURCE__V1__CAMERAS__INDEXCODE = "/api/resource/v1/cameras/indexCode"
    API__RESOURCE__V1__CAMERA__TIMERANGE = "/api/resource/v1/camera/timeRange"
    API__RESOURCE__V1__ALARMOUT__SEARCH = "/api/resource/v1/alarmOut/search"
    API__RESOURCE__V1__ALARMOUT__TIMERANGE = "/api/resource/v1/alarmOut/timeRange"
    API__VIDEO__V2__CAMERAS__PREVIEWURLS = "/api/video/v2/cameras/previewURLs"
    API__VIDEO__V2__CAMERAS__PLAYBACKURLS = "/api/video/v2/cameras/playbackURLs"
    API__VIDEO__V1__CAMERAS__TALKURLS = "/api/video/v1/cameras/talkURLs"
    API__VIDEO__V1__PTZS__CONTROLLING = "/api/video/v1/ptzs/controlling"
    API__VIDEO__V1__MANUALCAPTURE = "/api/video/v1/manualCapture"
    API__VIDEO__V1__PTZS__SELZOOM = "/api/video/v1/ptzs/selZoom"
    API__VIDEO__V1__RECORD__LOCK = "/api/video/v1/record/lock"
    API__VIDEO__V1__MANUALRECORD__START = "/api/video/v1/manualRecord/start"
    API__VIDEO__V1__MANUALRECORD__STOP = "/api/video/v1/manualRecord/stop"
    API__VIDEO__V1__MANUALRECORD__STATUS = "/api/video/v1/manualRecord/status"
    API__VIDEO__V1__MANUALRECORD__TASKID__SEARCH = "/api/video/v1/manualRecord/taskId/search"
    API__VIDEO__V1__PRESETS__ADDITION = "/api/video/v1/presets/addition"
    API__VIDEO__V1__PRESETS__SEARCHES = "/api/video/v1/presets/searches"
    API__VIDEO__V1__PRESETS__DELETION = "/api/video/v1/presets/deletion"
    API__VIDEO__V1__PRESETS__GET = "/api/video/v1/presets/get"
    API__VIDEO__V1__PICTUREINFOS = "/api/video/v1/pictureInfos"
    API__VIDEO__V1__EVENTS__PICTURE = "/api/video/v1/events/picture"
    API__VIDEO__V1__CRUISEROUTES__SEARCH = "/api/video/v1/cruiseRoutes/search"
    API__VIDEO__V1__CRUISEROUTES__UPDATE = "/api/video/v1/cruiseRoutes/update"
    API__VIDEO__V1__CRUISEROUTES__DELETE = "/api/video/v1/cruiseRoutes/delete"
    API__VIDEO__V1__CRUISEROUTES__CONTROLLING = "/api/video/v1/cruiseRoutes/controlling"
    API__VIDEO__V1__PICPARAMS__GET = "/api/video/v1/picParams/get"
    API__VIDEO__V1__SHOWSTRINGPARAMS__GET = "/api/video/v1/showStringParams/get"
    API__VIDEO__V1__VIDEOPARAMS__GET = "/api/video/v1/videoParams/get"
    API__VIDEO__V1__PICPARAMS__UDPATE = "/api/video/v1/picParams/udpate"
    API__VIDEO__V1__SHOWSTRINGPARAMS__UDPATE = "/api/video/v1/showStringParams/udpate"
    API__VIDEO__V1__VIDEOPARAMS__UDPATE = "/api/video/v1/videoParams/udpate"
    API__VIDEO__V1__ALARMOUT__STATUS__GET = "/api/video/v1/alarmOut/status/get"
    API__VIDEO__V1__ALARMOUT__STATUS__SET = "/api/video/v1/alarmOut/status/set"
    API__NMS__V1__RECORD__LIST = "/api/nms/v1/record/list"
    API__NMS__V1__VQD__LIST = "/api/nms/v1/vqd/list"
    API__NMS__V1__ONLINE__CAMERA__GET = "/api/nms/v1/online/camera/get"
    API__NMS__V1__ONLINE__ENCODE_DEVICE__GET = "/api/nms/v1/online/encode_device/get"
    API__TVMS__V1__TVWALL__ALLRESOURCES = "/api/tvms/v1/tvwall/allResources"
    API__TVMS__V1__TVWALL__SCENES = "/api/tvms/v1/tvwall/scenes"
    API__TVMS__V1__TVWALL__WNDS__GET = "/api/tvms/v1/tvwall/wnds/get"
    API__TVMS__V1__TVWALL__REALPLAY__ADD = "/api/tvms/v1/tvwall/realplay/add"
    API__TVMS__V1__TVWALL__REALPLAY__DELETE = "/api/tvms/v1/tvwall/realplay/delete"
    API__TVMS__V1__PUBLIC__TVWALL__SCENE__ADDITION = "/api/tvms/v1/public/tvwall/scene/addition"
    API__TVMS__V1__PUBLIC__TVWALL__SCENE__UPDATE = "/api/tvms/v1/public/tvwall/scene/update"
    API__TVMS__V1__PUBLIC__TVWALL__SCENE__DELETION = "/api/tvms/v1/public/tvwall/scene/deletion"
    API__TVMS__V1__PUBLIC__TVWALL__SCENE__SAVEAS = "/api/tvms/v1/public/tvwall/scene/saveAs"
    API__TVMS__V1__PUBLIC__TVWALL__SCENE__SWITCH = "/api/tvms/v1/public/tvwall/scene/switch"
    API__TVMS__V1__PUBLIC__TVWALL__ALARM__ADDITION = "/api/tvms/v1/public/tvwall/alarm/addition"
    API__TVMS__V1__PUBLIC__TVWALL__ALARM__DELETION = "/api/tvms/v1/public/tvwall/alarm/deletion"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWNDS__ADDITION = "/api/tvms/v1/public/tvwall/floatWnds/addition"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWNDS__DELETION = "/api/tvms/v1/public/tvwall/floatWnds/deletion"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWND__ZOOMIN = "/api/tvms/v1/public/tvwall/floatWnd/zoomIn"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWND__MOVE = "/api/tvms/v1/public/tvwall/floatWnd/move"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWND__LAYERCTRL = "/api/tvms/v1/public/tvwall/floatWnd/layerCtrl"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWND__ZOOMOUT = "/api/tvms/v1/public/tvwall/floatWnd/zoomOut"
    API__TVMS__V1__PUBLIC__TVWALL__FLOATWND__DIVISION = "/api/tvms/v1/public/tvwall/floatWnd/division"
    API__TVMS__V1__PUBLIC__TVWALL__MONITOR__DIVISION = "/api/tvms/v1/public/tvwall/monitor/division"
    API__ACPS__V1__AUTHDOWNLOAD__SPECIAL__PERSON__DIY = "/api/acps/v1/authDownload/special/person/diy"


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
