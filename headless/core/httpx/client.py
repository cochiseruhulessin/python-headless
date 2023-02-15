# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import httpx

from headless.types import IClient
from headless.types import ICredential
from ..resource import Resource # type: ignore
from .request import Request
from .response import Response


R = TypeVar('R', bound=Resource)
T = TypeVar('T', bound='Client')


class Client(IClient[httpx.Request, httpx.Response]):
    _client: httpx.AsyncClient
    response_class: type[Response] = Response
    request_class: type[Request] = Request

    def __init__(self, *, credential: ICredential | None = None, **kwargs: Any):
        self.credential = credential or self.credential
        self.params = kwargs
        self._client = httpx.AsyncClient(**kwargs)

    async def request_factory(self, method: str, url: str) -> httpx.Request:
        return self._client.build_request(
            method=method,
            url=url
        )

    async def send(self, request: Request) -> Response: # type: ignore
        return Response.fromimpl(request, await self._client.send(request.impl))

    async def __aenter__(self: T) -> T:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        await self._client.__aexit__(cls, *args)