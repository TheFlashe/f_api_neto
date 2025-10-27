from fastapi import FastAPI

import models
from schema import *
from lifespan import lifespan
from dependency import SessionDependency
import datetime
import crud

from sqlalchemy import select
from constans import SUCCESS_RESPONSE

app = FastAPI(
    title="Desc_API",
    lifespan=lifespan

)


@app.post('/advertisement', response_model=CreateAdvertisementResponse)
async def create_desc(desc: CreateAdvertisementRequest, session: SessionDependency):
    desc_orm_obj = models.Advertisement(**desc.model_dump(exclude_unset=True))
    await crud.add_item(session, desc_orm_obj)
    return desc_orm_obj.id_dict


@app.patch('/advertisement/{advertisement_id}', response_model=UpdateAdvertisementResponse)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest,
                               session: SessionDependency):
    advertisement_dict = advertisement_data.model_dump(exclude_unset=True, exclude="created_at")
    advertisement_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)

    for keys, vals in advertisement_dict.items():
        setattr(advertisement_obj, keys, vals)
    await crud.add_item(session, advertisement_obj)
    return SUCCESS_RESPONSE


@app.delete('/advertisement/{advertisement_id}', response_model=DeleteAdvertisementResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    desc_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    await crud.delete_item(session, desc_orm_obj)
    return SUCCESS_RESPONSE


@app.get('/advertisement/{advertisement_id}', response_model=GetAdvertisementResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    return advertisement_obj.dict


@app.get('/advertisement/', response_model=SearchAdvertisementResponse)
async def search_advertisement(author: str = None, price: int = None, description: str = None,
                               session: SessionDependency = SessionDependency):
    query = select(models.Advertisement)

    if author:
        query = query.where(models.Advertisement.author.ilike(f"%{author}%"))
    if description:
        query = query.where(models.Advertisement.description.ilike(f"%{description}%"))
    if price:
        query = query.where(models.Advertisement.price == price)

    query = query.limit(1000)
    result = await session.execute(query)
    descadverts = result.scalars().all()

    return SearchAdvertisementResponse(
        results=[GetAdvertisementResponse(**descadvert.dict) for descadvert in descadverts])
