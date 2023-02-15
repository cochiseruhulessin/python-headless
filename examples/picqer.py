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
from headless.ext.picqer import Order


async def main():
    params: dict[str, str]  = {
        'api_key': os.environ['MOLANO_PICQER_API_KEY'],
        'api_email': 'test@headless.python.dev.unimatrixone.io',
        'api_url': 'https://molano.picqer.com/api',
    }
    async with Client(**params) as client:
        for order in await client.list(Order):
            if not order.orderfields:
                continue
            print(repr(order))



if __name__ == '__main__':
    asyncio.run(main())