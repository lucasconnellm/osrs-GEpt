from typing import Optional
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_pagination import (
    Page,
    paginate,
)

from osrs_gept.container import OsrsContainer
from osrs_gept.models import (
    MappingInfo,
    MappingPayload,
    SlimMappingInfo,
    SlimMappingPayload,
)
from osrs_gept.pagination import Sort, SortDirection
from osrs_gept.wiki_client import WikiClient

router = APIRouter()


@router.get(
    "/mapping",
    description="Get a list of all items, their ids, and some metadata",
    response_model=Page[MappingInfo],
)
@inject
def get_mapping(
    sort_field: Optional[str] = None,
    sort_order: SortDirection = SortDirection.asc,
    *,
    wiki_client: WikiClient = Depends(
        Provide[OsrsContainer.wiki_client_factory],
    )
) -> MappingPayload:
    sort = None
    if sort_field is not None:
        sort = Sort(field=sort_field, order=sort_order)
    return paginate(wiki_client.get_mapping(sort=sort))


@router.get(
    "/mapping/slim",
    description="Get a list of all items, their ids, and names",
    response_model=Page[SlimMappingInfo],
)
@inject
def get_mapping_slim(
    sort_field: Optional[str] = None,
    sort_order: SortDirection = SortDirection.asc,
    *,
    wiki_client: WikiClient = Depends(
        Provide[OsrsContainer.wiki_client_factory],
    )
) -> SlimMappingPayload:
    sort = None
    if sort_field is not None:
        sort = Sort(field=sort_field, order=sort_order)
    return paginate(wiki_client.get_mapping_slim(sort=sort))
