# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from types import ModuleType
from typing import Any
from typing import TypeVar

from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse


Request = TypeVar('Request')


class Client(IClient[Request, Any]):
    impl: IClient[Request, Any]

    def __init__(
        self,
        impl: type[IClient[Request, Any]] | ModuleType,
        *args: Any,
        **kwargs: Any
    ):
        if isinstance(impl, ModuleType):
            impl = getattr(impl, 'Client')
        self.impl = impl(*args, **kwargs)

    async def request_factory(self, *args: Any, **kwargs: Any) -> Request:
        return await self.impl.request_factory(*args, **kwargs)

    async def send(self, request: IRequest[Any]) -> IResponse[Any, Any]:
        raise NotImplementedError

    async def __aenter__(self) -> 'ClientImplementation': # type: ignore
        await self.impl.__aenter__()
        return self

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        return await self.impl.__aexit__(cls, *args)