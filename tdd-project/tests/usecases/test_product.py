import asyncio
from decimal import Decimal
from uuid import UUID

import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import ProductUsecase


async def test_usecases_should_return_success(product_in, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_return_success(product_inserted, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_not_found(mongo_client):
    with pytest.raises(NotFoundException) as err:
        usecase = ProductUsecase(client=mongo_client)
        await usecase.get(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: UUID('1e4f214e-85f7-461a-89d0-a751a32e3bb9')"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success(mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.query()

    assert isinstance(result, list)
    assert len(result) > 1


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_filtered_by_price(mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.query(price_min=Decimal("5.000"), price_max=Decimal("8.000"))

    assert isinstance(result, list)
    assert len(result) > 0
    for product in result:
        assert product.price > Decimal("5.000")
        assert product.price < Decimal("8.000")


async def test_usecases_update_should_return_success(
    product_up, product_inserted, mongo_client
):
    product_up.price = Decimal("7.500")
    await asyncio.sleep(0.1)
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
    assert product_inserted.updated_at != result.updated_at


async def test_usecases_update_should_not_found(mongo_client):
    from store.schemas.product import ProductUpdate

    body = ProductUpdate(price=Decimal("7.500"))
    with pytest.raises(NotFoundException) as err:
        usecase = ProductUsecase(client=mongo_client)
        await usecase.update(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"), body=body)

    assert (
        err.value.message
        == "Product not found with filter: UUID('1e4f214e-85f7-461a-89d0-a751a32e3bb9')"
    )


async def test_usecases_delete_should_return_success(product_inserted, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_not_found(mongo_client):
    with pytest.raises(NotFoundException) as err:
        usecase = ProductUsecase(client=mongo_client)
        await usecase.delete(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: UUID('1e4f214e-85f7-461a-89d0-a751a32e3bb9')"
    )
