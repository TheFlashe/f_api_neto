from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class CreateAdvertisementResponse(IdResponse):
    pass


class SuccessResponse(BaseModel):
    status: Literal["success"]


class UpdateAdvertisementResponse(SuccessResponse):
    pass


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int | None
    author: str
    create_at: datetime | None
    updated_at: datetime | None


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class DeleteAdvertisementResponse(SuccessResponse):
    pass


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int | None = None
    author: str


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None
