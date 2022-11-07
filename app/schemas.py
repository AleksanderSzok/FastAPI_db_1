from typing import Optional

from pydantic import BaseModel, PositiveInt, constr


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=60)

    class Config:
        orm_mode = True


class Supplier_two(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[str]
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    Region: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]
    Fax: Optional[str]
    HomePage: Optional[str]

    class Config:
        orm_mode = True


class Category(BaseModel):
    CategoryID: int
    CategoryName: constr(max_length=40)

    class Config:
        orm_mode = True


class Product(BaseModel):
    ProductID: PositiveInt
    ProductName: constr(max_length=40)
    Category: Category
    Discontinued: int

    class Config:
        orm_mode = True


class SupplierPost(BaseModel):
    CompanyName: Optional[str]
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]

    class Config:
        orm_mode = True


class SupplierResponse(SupplierPost):
    SupplierID: PositiveInt
    Fax: Optional[str]
    HomePage: Optional[str]
