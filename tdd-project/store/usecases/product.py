from decimal import Decimal
from uuid import UUID

import pymongo
from bson import Decimal128
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings
from store.core.exceptions import NotFoundException
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUsecase:
    def __init__(self, client=None) -> None:
        self.client = client or AsyncIOMotorClient(settings.DATABASE_URL)
        self.database = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        return ProductOut(**result)

    async def query(self) -> list[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True, warnings=False)
        for key, value in update_data.items():
            if isinstance(value, Decimal):
                update_data[key] = Decimal128(str(value))

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
