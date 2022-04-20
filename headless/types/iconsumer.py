"""Declares :class:`IConsumer`."""
import functools
import types
import typing
from collections.abc import AsyncIterator

from .iclient import IClient
from .icredential import ICredential


class IConsumer:
    """The base class for all API consumer implementations. A consumer
    is the public interace of an API.
    """
    __module__: str = 'headless.types'
    client: IClient | None = None
    credential: ICredential
    schema: types.ModuleType
    server: str

    @classmethod
    async def session(
        cls,
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> AsyncIterator['IConsumer']:
        async with cls(*args , **kwargs) as session:
            yield session

    def __init__(
        self,
        schema: types.ModuleType,
        server: str,
        credential: ICredential
    ):
        self.schema = schema
        self.server = server
        self.credential = credential

    async def setup_context(self) -> None:
        raise NotImplementedError

    async def teardown_context(
        self,
        cls: type[BaseException],
        exception: BaseException,
        traceback: types.TracebackType
    ) -> bool:
        raise NotImplementedError

    async def __aenter__(self) -> 'IConsumer':
        await self.setup_context()
        return self

    async def __aexit__(
        self,
        cls: type[BaseException],
        exception: BaseException,
        traceback: types.TracebackType
    ) -> bool:
        return await self.teardown_context(cls, exception, traceback)

    def __getattr__(self, attname: str) -> typing.Any:
        if not hasattr(self.schema, attname):
            raise AttributeError(attname)
        return functools.partial(getattr(self.schema, attname), self.client)