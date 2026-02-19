from uuid import UUID

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings
from store.schemas.product import ProductIn
from tests.factories import product_data


@pytest.fixture
async def mongo_client():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    yield client
    client.close()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collection_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collection_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)
