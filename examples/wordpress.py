import asyncio
import functools
import os
import typing
from collections.abc import AsyncIterator

import headless


class WooCommerceInterface:
    version: str = 'v3'
    base_path: str = f'/wp-json/wc/{version}'

    async def get_products(
        self,
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
                'per_page': per_page
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
        async for product in api.get_products():
            print(f'{product["name"]}')


if __name__ == '__main__':
    asyncio.run(main())