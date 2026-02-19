from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings
from store.schemas.product import ProductIn, ProductOut


class ProductUsecase:
    def __init__(self, client: AsyncIOMotorClient | None = None) -> None:
        self.client: AsyncIOMotorClient = client or AsyncIOMotorClient(
            settings.DATABASE_URL
        )
        self.database = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        await self.collection.insert_one(body.model_dump())
        return ProductOut(**body.model_dump())


product_usecase = ProductUsecase()
