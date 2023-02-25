from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .crud import async_dbmanager_factory
from .database import get_db

router = APIRouter()


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    return await async_dbmanager_factory(session=db).get_suppliers()


@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierTwo)
async def get_shipper(supplier_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_supplier = await async_dbmanager_factory(session=db).get_supplier(supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_products(supplier_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_products = await async_dbmanager_factory(session=db).get_product(supplier_id)
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_products


@router.post("/suppliers", response_model=schemas.SupplierPost, status_code=201)
async def create_supplier(
    item: schemas.SupplierPost, db: AsyncSession = Depends(get_db)
):
    return await async_dbmanager_factory(session=db).post_supplier(item=item)


@router.put(
    "/suppliers/{supplier_id}", response_model=schemas.SupplierResponse, status_code=200
)
async def update_supplier(
    item: schemas.SupplierPost,
    supplier_id: PositiveInt,
    db: AsyncSession = Depends(get_db),
):
    update_item = await async_dbmanager_factory(session=db).put_supplier(
        item=item, supplier_id=supplier_id
    )
    if not update_item:
        raise HTTPException(status_code=404)
    return update_item


@router.delete("/suppliers/{supplier_id}", status_code=204, response_class=Response)
async def delete_supplier(supplier_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    supplier = await async_dbmanager_factory(session=db).delete_supplier(
        supplier_id=supplier_id
    )
    if not supplier:
        raise HTTPException(status_code=404)
    return


@router.get("/")
def start():
    return {"hello": "world"}
