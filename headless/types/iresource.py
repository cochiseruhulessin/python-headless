"""Declares :class:`IResource`."""
import typing
from collections.abc import AsyncIterator

import pydantic


class IResource:
    __module__: str = 'headless.types'
    model: type[pydantic.BaseModel]

    def list(
        self,
        path: str,
        params: pydantic.BaseModel | dict[str, typing.Any]
    ) -> AsyncIterator[dict[str, typing.Any]]:
        raise NotImplementedError

    async def retrieve(
        self,
        path: str,
        params: pydantic.BaseModel | dict[str, typing.Any]
    ) -> dict[str, typing.Any] | None:
        raise NotImplementedError