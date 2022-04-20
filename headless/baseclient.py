"""Declares :class:`BaseClient`."""
import types
import typing

import httpx

from .types import IClient
from .types import IRequest
from .types import IResponse


class BaseClient(IClient):
    __module__: str = 'headless'
    session: httpx.AsyncClient | None = None

    async def get(
        self,
        path: str,
        params: typing.Any = None
    ) -> IResponse:
        response = typing.cast(
            IResponse,
            await self.request(
                method='GET',
                path=path,
                params=params
            )
        )
        return response

    def get_absolute_url(self, path: str) -> str:
        return f"{self.server}{self.base_path}/{str.lstrip(path, '/')}"

    async def request(
        self,
        method: str,
        path: str,
        with_credential: bool = True,
        params: typing.Any = None
    ) -> httpx.Response:
        request = httpx.Request(
            method=method,
            url=self.get_absolute_url(path),
            params=params
        )
        if with_credential:
            await self.credential.authenticate(typing.cast(IRequest, request))
        assert self.session is not None # nosec
        return await self.session.send(request)

    async def __aenter__(self) -> 'BaseClient':
        if self.session is None:
            self.session = httpx.AsyncClient(
                base_url=f'{self.server}/{self.base_path}'
            )
            await self.session.__aenter__()
        return self

    async def __aexit__(
        self,
        cls: type[BaseException],
        exception: BaseException,
        traceback: types.TracebackType
    ) -> bool:
        if self.session is not None:
            session = self.session
            self.session = None
            await session.__aexit__(cls, exception, traceback)
        return False