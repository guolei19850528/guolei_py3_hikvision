# guolei-py3-hikvision
### a python3 library for hikvision
# ISC Example
```python
from guolei_py3_hikvision.library.isc import (Api, UrlSetting)

api = Api(
    host="your host",
    ak="your ak",
    sk="your sk"
)

result = api.post_json(
    path=UrlSetting.API__RESOURCE__V1__CARD__CARDLIST,
    json={
        "pageNo": 1,
        "pageSize": 10,
    },
)
```
