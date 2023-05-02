from typing import (
    List,
    Optional,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_pagination import (
    Page,
    paginate,
)

from osrs_gept.container import OsrsContainer
from osrs_gept.models import LatestInfoWithId
from osrs_gept.wiki_client import WikiClient

router = APIRouter()


@router.get(
    "/latest",
    description="Get the latest prices for all items",
    response_model=Page[LatestInfoWithId],
)
@inject
def get_latest(
    id_: Optional[int] = None,
    *,
    wiki_client: WikiClient = Depends(
        Provide[OsrsContainer.wiki_client_factory],
    )
) -> List[LatestInfoWithId]:
    return paginate(wiki_client.get_latest(id_))
