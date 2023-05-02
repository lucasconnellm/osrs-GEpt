from typing import (
    List,
    Optional,
)

import requests
from cachetools import (
    TTLCache,
    cached,
)

from osrs_gept.models import (
    LatestInfoWithId,
    LatestPayload,
    MappingInfo,
    MappingPayload,
    SlimMappingInfo,
    SlimMappingPayload,
)

WikiObjectsCache = TTLCache(maxsize=1024, ttl=60)


class WikiClient:
    def __init__(self, api_url: str, user_agent: str):
        self.api_url = api_url
        self.agent = user_agent

    @cached(WikiObjectsCache, key=lambda self, id_: id_)
    def get_latest(self, id_: Optional[int] = None) -> List[LatestInfoWithId]:
        params = {}
        if id_ is not None:
            params.update(id=id_)
        resp = requests.get(
            f"{self.api_url}/latest",
            params=params,
            headers={"User-Agent": self.agent},
        )
        resp.raise_for_status()
        returned_payload = LatestPayload.parse_obj(resp.json())
        return [
            LatestInfoWithId(id=id_, **info.dict())
            for id_, info in returned_payload.data.items()
        ]

    @cached(WikiObjectsCache, key=lambda self: "mapping")
    def get_mapping(self) -> MappingPayload:
        resp = requests.get(
            f"{self.api_url}/mapping",
            headers={"User-Agent": self.agent},
        )
        resp.raise_for_status()
        return [MappingInfo.parse_obj(item) for item in resp.json()]

    @cached(WikiObjectsCache, key=lambda self: "mapping_slim")
    def get_mapping_slim(self) -> SlimMappingPayload:
        full_mapping = self.get_mapping()
        return [
            SlimMappingInfo(id=item.id_, name=item.name)
            for item in full_mapping
        ]
