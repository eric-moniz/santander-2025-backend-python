from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUsecase:
    def __init__(self, client: AsyncIOMotorClient | None = None) -> None:
        self.client: AsyncIOMotorClient = client or AsyncIOMotorClient(
            settings.DATABASE_URL
        )
        self.database = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductOut(**body.model_dump())
        await self.collection.insert_one(product.model_dump())
        return product

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
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(
                message=f"Product not found with filter: UUID('{id}')"
            )

        return ProductUpdateOut(**result)


product_usecase = ProductUsecase()
