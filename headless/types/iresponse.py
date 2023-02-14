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
from typing import NoReturn
from typing import TypeVar

from .headers import Headers


W = TypeVar('W')
Request = TypeVar('Request')
Response = TypeVar('Response')

class IResponse(Generic[Request, Response]):
    """A wrapper for response objects."""
    __module__: str = 'headless.core'
    _request: Request
    _response: Response

    @classmethod
    def fromimpl(
        cls: type[W],
        request: Request,
        response: Response
    ) -> W:
        return cls(request, response)

    @property
    def headers(self) -> Headers:
        return self.get_headers()

    def __init__(self, request: Request, response: Response) -> None:
        self._request = request
        self._response = response

    def get_headers(self) -> Headers:
        raise NotImplementedError

    async def json(self) -> Any:
        raise NotImplementedError

    def raise_for_status(self) -> None | NoReturn:
        """Raises an exception according to the HTTP response
        status code, if applicable.
        """
        raise NotImplementedError