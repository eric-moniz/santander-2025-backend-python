from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import ProductUsecase
from tests.factories import product_data, products_data


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
async def client() -> AsyncClient:
    from store.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id):
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(product_in, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    return await usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    return [await usecase.create(body=product_in) for product_in in products_in]
