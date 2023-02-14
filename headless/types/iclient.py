# Copyright (C) 2022 Cochise Ruhulessin
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


Request = TypeVar('Request')
Response = TypeVar('Response')
M = TypeVar('M')
T = TypeVar('T', bound='IClient[Any, Any]')


class IClient(Generic[Request, Response]):
    """Specifies the interface for all API client implementations."""
    __module__: str = 'headless.types'

    async def request(self, *args: Any, **kwargs: Any) -> Response:
        raise NotImplementedError

    async def request_factory(
        self,
        method: str,
        url: str
    ) -> Request:
        raise NotImplementedError

    async def send(
        self,
        request: Request
    ) -> Response:
        raise NotImplementedError

    async def retrieve(self, model: type[M], resource_id: int | str) -> M:
        raise NotImplementedError

    async def __aenter__(self: T) -> T:
        raise NotImplementedError

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        raise NotImplementedError