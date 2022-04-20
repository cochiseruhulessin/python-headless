"""Declares :class:`IResponse`."""
from .json import JSONArray
from .json import JSONObject


class IResponse:
    __module__: str = 'headless.types'

    def json(self) -> JSONArray | JSONObject:
        raise NotImplementedError

    def raise_for_status(self) -> None:
        return None