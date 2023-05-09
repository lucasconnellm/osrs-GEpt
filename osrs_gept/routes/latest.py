from typing import (
    List,
    Optional,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi_pagination import (
    Page,
    paginate,
)
from pydantic import Field

from osrs_gept.container import OsrsContainer
from osrs_gept.models import LatestInfoWithId
from osrs_gept.pagination import Sort, SortDirection
from osrs_gept.wiki_client import WikiClient

router = APIRouter()


Page = Page.with_custom_options(
    size=Field(100, ge=1),
)


@router.get(
    "/latest",
    description="Get the latest prices for all items",
    response_model=Page[LatestInfoWithId],
)
@inject
def get_latest(
    id_: Optional[int] = None,
    sort_field: Optional[str] = None,
    sort_order: SortDirection = SortDirection.asc,
    *,
    wiki_client: WikiClient = Depends(
        Provide[OsrsContainer.wiki_client_factory],
    )
) -> Page[List[LatestInfoWithId]]:
    sort = None
    if sort_field is not None:
        if sort_field == "id":
            sort_field = "id_"
        sort = Sort(field=sort_field, order=sort_order)
    return paginate(wiki_client.get_latest(id_, sort))
