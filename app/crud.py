from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier)
        .filter(models.Supplier.SupplierID == supplier_id)
        .one_or_none()
    )


def get_product(db: Session, supplier_id: int):
    products_and_categories = (
        db.query(models.Product, models.Category)
        .filter(
            models.Product.SupplierID == supplier_id,
            models.Category.CategoryID == models.Product.CategoryID,
        )
        .order_by(desc(models.Product.ProductID))
        .all()
    )
    result = [get_product_aux(element) for element in products_and_categories]
    return result


def get_product_by_supplier_id(db: Session, supplier_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.SupplierID == supplier_id)
        .order_by(desc(models.Product.ProductID))
        .all()
    )


def get_product_aux(query_element):
    return {
        "ProductID": query_element[0].ProductID,
        "ProductName": query_element[0].ProductName,
        "Category": {
            "CategoryID": query_element[1].CategoryID,
            "CategoryName": query_element[1].CategoryName,
        },
        "Discontinued": query_element[0].Discontinued,
    }


def post_supplier(db: Session, item: schemas.SupplierPost):
    db_item = models.Supplier(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def put_supplier(db: Session, item: schemas.SupplierPost, supplier_id: int):
    supplier = (
        db.query(models.Supplier)
        .filter(models.Supplier.SupplierID == supplier_id)
        .one_or_none()
    )
    if not supplier:
        return
    for k, v in item.dict().items():
        if v:
            setattr(supplier, k, v)

    db.commit()
    db.refresh(supplier)
    return supplier
