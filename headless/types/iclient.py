# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar

from .icredential import ICredential
from .iresponse import IResponse
from .irequest import IRequest
from .nullcredential import NullCredential


Request = TypeVar('Request')
Response = TypeVar('Response')
M = TypeVar('M')
T = TypeVar('T', bound='IClient[Any, Any]')


class IClient(Generic[Request, Response]):
    """Specifies the interface for all API client implementations."""
    __module__: str = 'headless.types'
    credential: ICredential = NullCredential()
    request_class: type[IRequest[Request]]
    response_class: type[IResponse[Request, Response]]

    async def request(
        self,
        method: str,
        url: str,
        credential: ICredential | None = None
    ) -> IResponse[Request, Response]:
        request = await self._request_factory(
            method=method,
            url=url
        )
        await (credential or self.credential).add_to_request(request)
        return await self.send(request)

    async def request_factory(
        self,
        method: str,
        url: str
    ) -> Request:
        raise NotImplementedError

    async def send(self, request: IRequest[Request]) -> IResponse[Request, Response]:
        raise NotImplementedError

    async def retrieve(self, model: type[M], resource_id: int | str) -> M:
        raise NotImplementedError

    async def _request_factory(self, *args: Any, **kwargs: Any) -> IRequest[Request]:
        request = await self.request_factory(*args, **kwargs)
        return self.request_class.fromimpl(request)

    async def __aenter__(self: T) -> T:
        raise NotImplementedError

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        raise NotImplementedError