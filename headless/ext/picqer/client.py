# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any
from typing import NoReturn

from headless.core import httpx
from headless.types import IResponse
from .credential import PicqerCredential


class Client(httpx.Client):
    recover_ratelimit: bool = False

    def __init__(
        self,
        api_url: str,
        api_email: str,
        api_key: str,
        recover_ratelimit: bool = False
    ):
        self.recover_ratelimit = recover_ratelimit
        super().__init__(
            base_url=api_url,
            credential=PicqerCredential(api_email, api_key)
        )

    async def on_rate_limited(
        self,
        response: IResponse[Any, Any]
    ) -> NoReturn | IResponse[Any, Any]:
        # See https://picqer.com/en/api/response-codes
        if not self.recover_ratelimit:
            response.raise_for_status()
        self.logger.critical("Rate limited by Picqer, sleeping for 60 seconds")
        await asyncio.sleep(60)
        return await self.send(response.request)