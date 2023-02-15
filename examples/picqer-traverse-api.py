# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import os
from typing import Any

from headless.ext.picqer import Client
from headless.ext.picqer import PurchaseOrder


async def main():
    params: dict[str, Any]  = {
        'api_key': os.environ['MOLANO_PICQER_API_KEY'],
        'api_email': 'test@headless.python.dev.unimatrixone.io',
        'api_url': 'https://molano.picqer.com/api'
    }
    async with Client(**params) as client:
        orders: list[PurchaseOrder] = [x async for x in client.list(PurchaseOrder)]
        assert orders
        assert orders[0].idsupplier is not None
        order = orders[0]

        # Before awaiting, the attribute contains a wrapper.
        print(repr(order.supplier))

        # After awaiting the object, the resource becomes available.
        await order.supplier
        print(repr(order.supplier))



if __name__ == '__main__':
    asyncio.run(main())