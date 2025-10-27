from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class CreateDescResponse(IdResponse):
    pass


class SuccessResponse(BaseModel):
    status: Literal["success"]


class UpdateDescResponse(SuccessResponse):
    pass


class GetDescResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int | None
    author: str
    create_at: datetime | None
    updated_at: datetime | None


class SearchDescResponse(BaseModel):
    results: list[GetDescResponse]


class DeleteDescResponse(SuccessResponse):
    pass


class CreateDescRequest(BaseModel):
    title: str
    description: str
    price: int | None = None
    author: str


class UpdateDescRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None
