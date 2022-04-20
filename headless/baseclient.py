"""Declares :class:`BaseClient`."""
import types
import typing
import urllib.parse

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
        return await self.request(
                method='GET',
                path=path,
                params=params
            )

    async def put(
        self,
        path: str,
        params: typing.Any = None,
        json: dict[str, typing.Any] | None = None
    ) -> IResponse:
        return await self.request(
            method='PUT',
            path=path,
            params=params,
            json=json
        )

    def get_absolute_url(self, path: str) -> str:
        return f"{self.server}{self.base_path}/{str.lstrip(path, '/')}"

    async def request(
        self,
        method: str,
        path: str,
        with_credential: bool = True,
        params: typing.Any = None,
        json: dict[str, typing.Any] | None = None
    ) -> IResponse:
        url = path
        if self.is_relative_url(url):
            url = self.get_absolute_url(path)
        request = httpx.Request(
            method=method,
            url=url,
            params=params,
            json=json
        )
        if with_credential:
            await self.credential.authenticate(typing.cast(IRequest, request))
        assert self.session is not None # nosec
        return typing.cast(
            IResponse,
            await self.session.send(request)
        )

    def is_relative_url(self, url: str) -> bool:
        p = urllib.parse.urlparse(url)
        return not bool(p.scheme and p.netloc)

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