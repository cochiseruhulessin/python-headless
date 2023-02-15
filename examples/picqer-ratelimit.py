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
from typing import Awaitable

from headless.ext.picqer import Client
from headless.ext.picqer import User


async def main():
    params: dict[str, Any]  = {
        'api_key': os.environ['MOLANO_PICQER_API_KEY'],
        'api_email': 'test@headless.python.dev.unimatrixone.io',
        'api_url': 'https://molano.picqer.com/api'
    }
    async with Client(**params) as client:
        requests: list[Awaitable[User]] = []
        for _ in range(512):
            requests.append(client.retrieve(User, 13631))
        await asyncio.gather(*requests)



if __name__ == '__main__':
    asyncio.run(main())