from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: AsyncSession = Depends(get_db)):
    suppliers = await crud.get_suppliers(db)
    return [supplier[0] for supplier in suppliers]


@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierTwo)
async def get_shipper(supplier_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_supplier = await crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.Product])
async def get_products(supplier_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_products = await crud.get_product(db, supplier_id)
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_products


@router.post("/suppliers", response_model=schemas.SupplierPost, status_code=201)
async def create_supplier(
    item: schemas.SupplierPost, db: AsyncSession = Depends(get_db)
):
    return await crud.post_supplier(db=db, item=item)


@router.put(
    "/suppliers/{supplier_id}", response_model=schemas.SupplierResponse, status_code=200
)
async def update_supplier(
    item: schemas.SupplierPost, supplier_id: int, db: AsyncSession = Depends(get_db)
):
    update_item = await crud.put_supplier(db=db, item=item, supplier_id=supplier_id)
    if not update_item:
        raise HTTPException(status_code=404)
    return update_item


@router.delete("/suppliers/{supplier_id}", status_code=204, response_class=Response)
async def delete_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    supplier = await crud.get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404)
    await db.delete(supplier)
    await db.commit()
    return


@router.get("/")
def start():
    return {"hello": "world"}
