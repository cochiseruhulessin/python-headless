# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import uuid
from typing import Any
from typing import Generic
from typing import TypeVar

W = TypeVar('W')
Request = TypeVar('Request')


class IRequest(Generic[Request]):
    """A wrapper for response objects."""
    __module__: str = 'headless.core'
    _request: Request

    @classmethod
    def fromimpl(cls: type[W], request: Request) -> W:
        return cls(request)

    @property
    def id(self) -> str:
        return self._id

    @property
    def impl(self) -> Request:
        return self._request

    @property
    def url(self) -> str:
        return self.get_url()

    def __init__(self, request: Request) -> None:
        self._id = str(uuid.uuid4())
        self._request = request

    def add_header(self, name: str, value: str) -> None:
        raise NotImplementedError

    def get_url(self) -> str:
        raise NotImplementedError

    async def retry(self) -> Any:
        pass