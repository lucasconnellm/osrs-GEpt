from typing import (
    Dict,
    List,
    Optional,
)

from humps.camel import case
from pydantic import (
    BaseModel,
    Field,
)


class LatestInfo(BaseModel):
    class Config:
        alias_generator = case

    high: Optional[int] = Field(
        description="The latest high price transaction",
    )
    high_time: Optional[int] = Field(
        description="The time of the latest high price transaction",
    )
    low: Optional[int] = Field(description="The latest low price transaction")
    low_time: Optional[int] = Field(
        description="The time of the latest low price transaction",
    )


class LatestPayload(BaseModel):
    data: Dict[int, LatestInfo] = Field(
        description="The latest price information for each item. "
        + "The key is the item ID.",
    )


class LatestInfoWithId(LatestInfo):
    id_: int = Field(alias="id", description="The item's ID")


class MappingInfo(BaseModel):
    examine: str = Field(description="The item's examine text")
    id_: int = Field(alias="id", description="The item's ID")
    icon: str = Field(description="The item's icon URL")
    members: bool = Field(
        description="Whether or not the item is members-only",
    )
    name: str = Field(description="The item's name")
    lowalch: Optional[int] = Field(description="The item's low alchemy value")
    highalch: Optional[int] = Field(
        description="The item's high alchemy value",
    )
    limit: Optional[int] = Field(description="The item's trade limit")
    value: Optional[int] = Field(description="The item's value")


MappingPayload = List[MappingInfo]


class SlimMappingInfo(BaseModel):
    class Config:
        alias_generator = case
        allow_population_by_field_name = True
        allow_population_by_alias = True

    id_: int = Field(alias="id", description="The item's ID")
    name: str = Field(description="The item's name")


SlimMappingPayload = List[SlimMappingInfo]
