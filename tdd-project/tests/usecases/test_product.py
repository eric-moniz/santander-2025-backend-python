from store.schemas.product import ProductOut
from store.usecases.product import ProductUsecase


async def test_usecases_should_return_success(product_in, mongo_client):
    usecase = ProductUsecase(client=mongo_client)
    result = await usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
