from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import get_db

router = APIRouter()


@router.get("/suppliers", response_model=List[schemas.Supplier])
def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier_two)
def get_shipper(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get(
    "/suppliers/{supplier_id}/products", response_model=List[schemas.ProductAndCategory]
)
def get_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_products = crud.get_product(db, supplier_id)
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_products


@router.get("/sup/{id}/products", response_model=List[schemas.Product])
def get_pro(id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_supplier_id(supplier_id=id, db=db)


@router.post("/suppliers", response_model=schemas.SupplierResponse, status_code=201)
def create_supplier(item: schemas.SupplierPost, db: Session = Depends(get_db)):
    return crud.post_supplier(db=db, item=item)


@router.put(
    "/suppliers/{supplier_id}", response_model=schemas.SupplierResponse, status_code=200
)
def update_supplier(
    item: schemas.SupplierPost, supplier_id: int, db: Session = Depends(get_db)
):
    update_item = crud.put_supplier(db=db, item=item, supplier_id=supplier_id)
    if not update_item:
        raise HTTPException(status_code=404)
    return update_item


@router.delete("/suppliers/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = (
        db.query(models.Supplier)
        .filter(models.Supplier.SupplierID == supplier_id)
        .one_or_none()
    )
    if not supplier:
        raise HTTPException(status_code=404)
    db.delete(supplier)
    db.commit()


@router.get("/")
def start():
    return {"hello": "world"}

