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

from headless.ext.picqer import Client
from headless.ext.picqer import PurchaseOrder
from headless.ext.picqer import User
from headless.ext.picqer import Warehouse


async def main():
    params: dict[str, str]  = {
        'api_key': os.environ['MOLANO_PICQER_API_KEY'],
        'api_email': 'test@headless.python.dev.unimatrixone.io',
        'api_url': 'https://molano.picqer.com/api',
    }
    async with Client(**params) as client:
        print(repr(await client.retrieve(User, 13631)))
        print(repr(await client.retrieve(Warehouse, 6790)))
        order = await client.retrieve(PurchaseOrder, 1503164)
        print(order)
        print(await order.get_purchaser())


if __name__ == '__main__':
    asyncio.run(main())