import asyncio
import functools
import os
import typing
from collections.abc import AsyncIterator

import headless


class WooCommerceInterface:
    version: str = 'v3'
    base_path: str = f'/wp-json/wc/{version}'

    async def update_stock(
        self,
        consumer: headless.types.IConsumer,
        client: headless.types.IClient,
        product_id: int,
        stock_quantity: int
    ) -> None:
        await client.put(
            f'products/{product_id}',
            json={
                'manage_stock': True,
                'stock_quantity': stock_quantity
            }
        )

    async def get_products(
        self,
        consumer: headless.types.IConsumer,
        client: headless.types.IClient
    ) -> AsyncIterator[headless.types.JSONObject]:
        async for dto in self.iterate(client=client, path='products'):
            yield dto

    async def iterate(
        self,
        client: headless.types.IClient,
        path: str,
        page: int = 1,
        per_page: int = 10
    ) -> AsyncIterator[headless.types.JSONObject]:
        while True:
            params = {
                'page': page,
                'per_page': per_page,
                'context': "edit"
            }
            response = await client.get(path, params=params)
            objects = response.json()
            if not objects:
                break
            for dto in objects:
                yield typing.cast(headless.types.JSONObject, dto)
            page += 1
            if len(objects) < per_page:
                break


Consumer = functools.partial(
    headless.Consumer,
    schema=WooCommerceInterface(),
    server=os.environ['WOOCOMMERCE_BASE_URL'],
    credential=headless.credentials.BasicAuthCredential(
        username=os.environ['WOOCOMMERCE_API_KEY'],
        password=os.environ['WOOCOMMERCE_API_SECRET']
    )
)


async def main():
    async with Consumer() as api:
        await api.update_stock(54, 555)


if __name__ == '__main__':
    asyncio.run(main())