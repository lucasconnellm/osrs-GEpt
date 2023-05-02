from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi_pagination import Page, paginate

from osrs_gept.container import OsrsContainer
from osrs_gept.models import MappingInfo, MappingPayload, SlimMappingInfo, SlimMappingPayload
from osrs_gept.wiki_client import WikiClient

router = APIRouter()


@router.get('/mapping', description='Get a list of all items, their ids, and some metadata', response_model=Page[MappingInfo])
@inject
def get_mapping(*, wiki_client: WikiClient = Depends(Provide[OsrsContainer.wiki_client_factory])) -> MappingPayload:
    return paginate(wiki_client.get_mapping())

@router.get('/mapping/slim', description='Get a list of all items, their ids, and names', response_model=Page[SlimMappingInfo])
@inject
def get_mapping_slim(*, wiki_client: WikiClient = Depends(Provide[OsrsContainer.wiki_client_factory])) -> SlimMappingPayload:
    return paginate(wiki_client.get_mapping_slim())