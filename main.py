from fastapi import FastAPI

import models
from schema import *
from lifespan import lifespan
from dependancy import SessionDependancy
import datetime
import crud

from sqlalchemy import select
from constans import SUCCESS_RESPONSE

app = FastAPI(
    title="Desc_API",
    lifespan=lifespan

)


@app.post('/api/desc', response_model=CreateDescResponse)
async def create_desc(desc: CreateDescRequest, session: SessionDependancy):
    desc_orm_obj = models.Desc(**desc.model_dump(exclude_unset=True))
    await crud.add_item(session, desc_orm_obj)
    return desc_orm_obj.id_dict


@app.patch('/api/desc/{desc_id}', response_model=UpdateDescResponse)
async def update_desc(desc_id: int, desc_data: UpdateDescRequest, session: SessionDependancy):
    desc_dict = desc_data.model_dump(exclude_unset=True, exclude="create_at")
    desc_obj = await crud.get_item_by_id(session, models.Desc, desc_id)

    for keys, vals in desc_dict.items():
        setattr(desc_obj, keys, vals)
    await crud.add_item(session, desc_obj)
    return SUCCESS_RESPONSE


@app.delete('/api/desc/{desc_id}', response_model=DeleteDescResponse)
async def delete_desc(desc_id: int, session: SessionDependancy):
    desc_orm_obj = await crud.get_item_by_id(session, models.Desc, desc_id)
    await crud.delete_item(session, desc_orm_obj)
    return SUCCESS_RESPONSE


@app.get('/api/desc/{desc_id}', response_model=GetDescResponse)
async def get_desc(desc_id: int, session: SessionDependancy):
    desc_obj = await crud.get_item_by_id(session, models.Desc, desc_id)
    return desc_obj.dict


@app.get('/api/desc/', response_model=SearchDescResponse)
async def search_desc(author: str = None, price: int = None,
                      session: SessionDependancy = SessionDependancy):
    query = select(models.Desc)

    if author:
        query = query.where(models.Desc.author.ilike(f"%{author}%"))
    if price:
        query = query.where(models.Desc.price == price)
    query = query.limit(1000)
    result = await session.execute(query)
    descs = result.scalars().all()

    return SearchDescResponse(results=[GetDescResponse(**desc.dict) for desc in descs])
