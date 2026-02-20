from datetime import datetime

from pydantic import UUID4, BaseModel, Field

from store.schemas.base import BaseSchemaMixin


class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: float = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin): ...


class ProductOut(ProductIn):
    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()


class ProductUpdate(ProductBase):
    quantity: int | None = Field(None, description="Product quantity")
    price: float | None = Field(None, description="Product price")
    status: bool | None = Field(None, description="Product status")


class ProductUpdateOut(ProductUpdate): ...
