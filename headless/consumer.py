"""Declares :class:`Consumer`."""
import types

from .baseclient import BaseClient
from .types import IConsumer


class Consumer(IConsumer):
    __module__: str = 'headless'
    _must_teardown: bool = False

    async def setup_context(self) -> None:
        if self.client is None:
            self.client = BaseClient(
                server=self.server,
                base_path=self.schema.base_path,
                credential=self.credential
            )
            await self.client.__aenter__()
            self._must_teardown = True

    async def teardown_context(
        self,
        cls: type[BaseException],
        exception: BaseException,
        traceback: types.TracebackType
    ) -> bool:
        if self._must_teardown:
            assert self.client is not None # nosec
            self._must_teardown = False
            await self.client.__aexit__(cls, exception, traceback)
        return False