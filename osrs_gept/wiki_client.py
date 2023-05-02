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
from osrs_gept.pagination import Sort, SortDirection

WikiObjectsCache = TTLCache(maxsize=1024, ttl=60)


class WikiClient:
    def __init__(self, api_url: str, user_agent: str):
        self.api_url = api_url
        self.agent = user_agent

    @cached(WikiObjectsCache, key=lambda self, id_: id_)
    def _get_latest(self, id_: Optional[int] = None) -> List[LatestInfoWithId]:
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
    
    @cached(WikiObjectsCache, key=lambda self, id_, sort: (id_, str(sort)))
    def get_latest(self, id_: Optional[int] = None, sort: Optional[Sort] = None) -> List[LatestInfoWithId]:
        full_resp = self._get_latest(id_)
        if sort is None:
            return full_resp
        return sorted(full_resp, key=lambda item: getattr(item, sort.field) if getattr(item, sort.field) else 0, reverse=sort.order == SortDirection.desc)

    @cached(WikiObjectsCache, key=lambda self: 'mapping')
    def _get_mapping(self) -> MappingPayload:
        resp = requests.get(
            f"{self.api_url}/mapping",
            headers={"User-Agent": self.agent},
        )
        resp.raise_for_status()
        return [MappingInfo.parse_obj(item) for item in resp.json()]

    @cached(WikiObjectsCache, key=lambda self, sort: str(sort))
    def get_mapping(self, sort: Optional[Sort] = None) -> MappingPayload:
        full_resp = self._get_mapping()
        if sort is None:
            return full_resp
        sort_type = int
        if sort.field in ('name', 'description', 'examine', 'wiki_url', 'icon'):
            sort_type = str
        elif sort.field in ('members'):
            sort_type = bool
        sort_key = lambda item: getattr(item, sort.field) if getattr(item, sort.field) else sort_type()
        return sorted(full_resp, key=sort_key, reverse=sort.order == SortDirection.desc)

    @cached(WikiObjectsCache, key=lambda self: 'mapping_slim')
    def _get_mapping_slim(self) -> SlimMappingPayload:
        full_mapping = self._get_mapping()
        return [
            SlimMappingInfo(id=item.id_, name=item.name)
            for item in full_mapping
        ]

    @cached(WikiObjectsCache, key=lambda self, sort: str(sort))
    def get_mapping_slim(self, sort: Optional[Sort] = None) -> SlimMappingPayload:
        full_resp = self._get_mapping_slim()
        if sort is None:
            return full_resp
        if sort.field in ('name', 'description', 'examine', 'wiki_url', 'icon'):
            sort_type = str
        elif sort.field in ('members'):
            sort_type = bool
        sort_key = lambda item: getattr(item, sort.field) if getattr(item, sort.field) else sort_type()
        return sorted(full_resp, key=sort_key, reverse=sort.order == SortDirection.desc)
