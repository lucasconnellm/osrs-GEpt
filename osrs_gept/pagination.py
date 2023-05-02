from enum import Enum

from fastapi_pagination import Page, paginate
from humps.camel import case
from pydantic import BaseModel


OsrsPage = Page


class SortDirection(str, Enum):
    asc = "ASC"
    desc = "DESC"

class Sort(BaseModel):
    field: str
    order: SortDirection = SortDirection.asc

    def __str__(self):
        return f"{self.field}:{self.order.value}"
