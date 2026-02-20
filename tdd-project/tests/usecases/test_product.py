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


async def test_usecases_get_return_success(product_id, product_inserted, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.get(id=product_id)

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


async def test_usecases_query_should_return_success(mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.query()

    assert isinstance(result, list)


async def test_usecases_update_should_return_success(
    product_id, product_up, product_inserted, mongo_client
):
    product_up.price = 7.500
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.update(id=product_id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
