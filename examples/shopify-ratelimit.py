# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
import os
from typing import Any
from typing import Awaitable

from headless.ext.shopify import AdminClient
from headless.ext.shopify.v2023_1 import Order


async def main():
    logger: logging.Logger = logging.getLogger('headless.client')
    logger.setLevel(logging.INFO)
    params: dict[str, Any]  = {
        'access_token': os.environ['SHOPIFY_ACCESS_TOKEN'],
        'domain': 'molano-uplink.myshopify.com'
    }
    async with AdminClient(**params) as client:
        requests: list[Awaitable[Order]] = []
        for _ in range(50):
            requests.append(client.retrieve(Order, 5273119949113))
        orders = await asyncio.gather(*requests)
        print(orders[-1].json(indent=2))



if __name__ == '__main__':
    asyncio.run(main())