# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import httpx
from headless.types import IRequest


class Request(IRequest[httpx.Request]):
    __module__: str = 'headless.core.httpx'

    def add_header(self, name: str, value: str) -> None:
        self._request.headers[name] = value