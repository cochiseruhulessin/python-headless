# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import pydantic

from headless.types import IClient
from .resourcemeta import ResourceMeta
from .resourcemetaclass import ResourceMetaclass


T = TypeVar('T', bound='Resource')
Request = TypeVar('Request')
Response = TypeVar('Response')


class Resource(pydantic.BaseModel, metaclass=ResourceMetaclass):
    """The base class for all resource implementations."""
    __abstract__: bool = True
    _client: IClient[Any, Any] = pydantic.PrivateAttr()
    _meta: ResourceMeta = pydantic.PrivateAttr()

    @classmethod
    def process_response(cls, action: str, data: dict[str, Any]) -> dict[str, Any]:
        """Process response data prior to parsing using the declared model."""
        return data