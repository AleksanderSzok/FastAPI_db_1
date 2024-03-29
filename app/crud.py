from typing import List, Optional, Tuple, Union, Dict

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models
from . import schemas


class AsyncDbManager:
    def __init__(self):
        self.db = None

    async def get_suppliers(self) -> List[models.Supplier]:
        query = select(models.Supplier).order_by(models.Supplier.SupplierID)
        suppliers = await self.db.execute(query)
        return [supplier[0] for supplier in suppliers]

    async def get_supplier(self, supplier_id: int) -> Optional[models.Supplier]:
        query = select(models.Supplier).filter(
            models.Supplier.SupplierID == supplier_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_product(self, supplier_id: int) -> List[Dict[str, Union[str, int]]]:
        query = (
            select(models.Product, models.Category)
            .filter(
                models.Product.SupplierID == supplier_id,
                models.Category.CategoryID == models.Product.CategoryID,
            )
            .order_by(desc(models.Product.ProductID))
        )
        products_and_categories = await self.db.execute(query)
        result = [self.get_product_aux(element) for element in products_and_categories]
        return result

    @staticmethod
    def get_product_aux(
        query_element: Tuple[Union[models.Product, models.Category]]
    ) -> Dict[str, Union[str, int]]:
        return {
            "ProductID": query_element[0].ProductID,
            "ProductName": query_element[0].ProductName,
            "Category": {
                "CategoryID": query_element[1].CategoryID,
                "CategoryName": query_element[1].CategoryName,
            },
            "Discontinued": query_element[0].Discontinued,
        }

    async def post_supplier(self, item: schemas.SupplierPost) -> models.Supplier:
        db_item = models.Supplier(**item.dict())
        self.db.add(db_item)
        await self.db.commit()
        return db_item

    async def put_supplier(
        self, item: schemas.SupplierPost, supplier_id: int
    ) -> Optional[models.Supplier]:
        supplier = await self.get_supplier(supplier_id=supplier_id)
        if not supplier:
            return
        for k, v in item.dict().items():
            if v:
                setattr(supplier, k, v)

        await self.db.commit()
        return supplier

    async def delete_supplier(self, supplier_id: int) -> Optional[models.Supplier]:
        supplier = await self.get_supplier(supplier_id=supplier_id)
        if not supplier:
            return
        await self.db.delete(supplier)
        await self.db.commit()
        return supplier


def async_dbmanager_factory(
    session: AsyncSession, _singleton: AsyncDbManager = AsyncDbManager()
) -> AsyncDbManager:
    _singleton.db = session
    return _singleton
