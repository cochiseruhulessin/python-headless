# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generator
from typing import Callable
from typing import TypeVar

import pydantic

from .iresponse import IResponse
from .resourcexceptiontype import ResourceExceptionType


T = TypeVar('T', bound='ResourceException')


class ResourceException(BaseException, metaclass=ResourceExceptionType):
    __abstract__: bool = True
    __module__: str = 'headless.types'
    model: type[pydantic.BaseModel]
    instance: pydantic.BaseModel

    @classmethod
    def __get_validators__(cls: type[T]) -> Generator[Callable[..., T], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls: type[T], v: dict[str, Any]) -> T:
        return cls(cls.model.parse_obj(v))

    @classmethod
    def parse_obj(cls: type[T], obj: Any) -> T:
        return cls(cls.model.parse_obj(obj))

    @classmethod
    async def parse_response(cls: type[T], response: IResponse[Any, Any]) -> T | None:
        try:
            return cls.parse_obj(await response.json())
        except pydantic.ValidationError:
            return None

    def __init__(self, instance: pydantic.BaseModel):
        self.instance = instance

    def __repr__(self) -> str:
        return repr(self.instance)