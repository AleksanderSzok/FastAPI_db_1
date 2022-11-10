from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models
from . import schemas


async def get_suppliers(db: AsyncSession):
    query = select(models.Supplier).order_by(models.Supplier.SupplierID)
    return await db.execute(query)


async def get_supplier(db: AsyncSession, supplier_id: int):
    query = select(models.Supplier).filter(models.Supplier.SupplierID == supplier_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_product(db: AsyncSession, supplier_id: int):
    query = (
        select(models.Product, models.Category)
        .filter(
            models.Product.SupplierID == supplier_id,
            models.Category.CategoryID == models.Product.CategoryID,
        )
        .order_by(desc(models.Product.ProductID))
    )
    products_and_categories = await db.execute(query)
    result = [get_product_aux(element) for element in products_and_categories]
    return result


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


async def post_supplier(db: AsyncSession, item: schemas.SupplierPost):
    db_item = models.Supplier(**item.dict())
    db.add(db_item)
    await db.commit()
    return db_item


async def put_supplier(db: AsyncSession, item: schemas.SupplierPost, supplier_id: int):
    supplier = await get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        return
    for k, v in item.dict().items():
        if v:
            setattr(supplier, k, v)

    await db.commit()
    return supplier
