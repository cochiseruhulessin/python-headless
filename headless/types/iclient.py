# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar

from .headers import Headers
from .icredential import ICredential
from .iresponse import IResponse
from .irequest import IRequest
from .nullcredential import NullCredential


Request = TypeVar('Request')
Response = TypeVar('Response')
M = TypeVar('M')
T = TypeVar('T', bound='IClient[Any, Any]')


class IClient(Generic[Request, Response]):
    """Specifies the interface for all API client implementations."""
    __module__: str = 'headless.types'
    credential: ICredential = NullCredential()
    request_class: type[IRequest[Request]]
    response_class: type[IResponse[Request, Response]]

    def check_json(self, headers: Headers):
        # TODO: Abstract this to a separate class.
        if headers.get('Content-Type') != 'application/json':
            raise TypeError(
                'Invalid response content type: '
                '{response.headers.get("Content-Type")}'
            )

    async def request(
        self,
        method: str,
        url: str,
        credential: ICredential | None = None
    ) -> IResponse[Request, Response]:
        request = await self._request_factory(
            method=method,
            url=url
        )
        await (credential or self.credential).add_to_request(request)
        return await self.send(request)

    async def retrieve(self, model: type[M], resource_id: int | str) -> M:
        """Discover the API endpoint using the class configuration
        and retrieve a single instance using the HTTP GET verb.
        """
        response = await self.request(
            method='GET',
            url=model._meta.get_retrieve_url(resource_id) # type: ignore
        )
        response.raise_for_status()
        self.check_json(response.headers)
        data = self.process_response('retrieve', await response.json())
        return self.resource_factory(model, 'retrieve', data)

    def process_response(self, action: str, data: dict[str, Any] | list[Any]) -> dict[str, Any]:
        """Hook to transform response data."""
        return data

    def resource_factory(self, model: type[M], action, data: dict[str, Any]) -> M:
        resource = model.parse_obj(model.process_response(action, data))
        resource._client = self # type: ignore
        return resource

    async def _request_factory(self, *args: Any, **kwargs: Any) -> IRequest[Request]:
        request = await self.request_factory(*args, **kwargs)
        return self.request_class.fromimpl(request)

    async def request_factory(
        self,
        method: str,
        url: str
    ) -> Request:
        raise NotImplementedError

    async def send(self, request: IRequest[Request]) -> IResponse[Request, Response]:
        raise NotImplementedError

    async def __aenter__(self: T) -> T:
        raise NotImplementedError

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        raise NotImplementedError

    async def list(self, model: type[M]) -> list[M]:
        """Discover the API endpoint using the class configuration
        and retrieve a list of instances using the HTTP GET verb.
        """
        response = await self.request(
            method='GET',
            url=model._meta.get_list_url()
        )
        response.raise_for_status()
        self.check_json(response.headers)
        data = self.process_response('list', await response.json())
        return [
            self.resource_factory(model, 'list', x)
            for x in data
        ]