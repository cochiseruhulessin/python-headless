# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import logging
from collections.abc import Iterable
from collections.abc import Mapping
from typing import Any
from typing import Generic
from typing import Generator
from typing import NoReturn
from typing import TypeVar

import pydantic

from .headers import Headers
from .ibackoff import IBackoff
from .icredential import ICredential
from .iresource import IResource
from .iresponse import IResponse
from .irequest import IRequest
from .nullbackoff import NullBackoff
from .nullcredential import NullCredential


Request = TypeVar('Request')
Response = TypeVar('Response')
M = TypeVar('M', bound=IResource)
T = TypeVar('T', bound='IClient[Any, Any]')


class IClient(Generic[Request, Response]):
    """Specifies the interface for all API client implementations."""
    __module__: str = 'headless.types'
    backoff: IBackoff = NullBackoff()
    credential: ICredential = NullCredential()
    request_class: type[IRequest[Request]]
    response_class: type[IResponse[Request, Response]]
    logger: logging.Logger = logging.getLogger('headless.client')

    def check_json(self, headers: Headers):
        # TODO: Abstract this to a separate class.
        content_type = headers.get('Content-Type') or ''
        if not str.startswith(content_type, 'application/json'):
            raise TypeError(
                'Invalid response content type: '
                f'{headers.get("Content-Type")}'
            )

    async def persist(
        self,
        model: type[M],
        instance: M
    ) -> M:
        response = await self.request(
            method=model._meta.persist_method,
            url=instance.get_persist_url(),
            json=instance.dict()
        )
        response.raise_for_status()
        return instance

    async def request(
        self,
        method: str,
        url: str,
        credential: ICredential | None = None,
        json: list[Any] | dict[str, Any] | None = None
    ) -> IResponse[Request, Response]:
        headers: dict[str, str] = {}
        if json is not None:
            headers['Content-Type'] = 'application/json'
        request = await self._request_factory(
            method=method,
            url=url,
            headers=headers,
            json=json
        )
        await (credential or self.credential).add_to_request(request)
        response = await self.send(request)
        if response.status_code == 429:
            response = await self.on_rate_limited(response)
        return response

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

    async def on_rate_limited(
        self,
        response: IResponse[Any, Any]
    ) -> NoReturn | IResponse[Any, Any]:
        """Invoked when the endpoint returns a ``429`` status code, indicating that
        it is rate limited. The default implementation raises an exception, but
        subclasses may override this method to return a response object.
        """
        return await self.backoff.retry(self, response.request, response)

    def process_response(self, action: str, data: dict[str, Any] | list[Any]) -> dict[str, Any]:
        """Hook to transform response data."""
        return data

    def resource_factory(self, model: type[M], action, data: dict[str, Any]) -> M:
        resource = model.parse_obj(model.process_response(action, data))
        self._inject_client(resource)
        return resource

    async def request_factory(
        self,
        method: str,
        url: str,
        json: list[Any] | dict[str, Any] | None = None,
        headers: dict[str, str] | None = None
    ) -> Request:
        raise NotImplementedError

    async def send(self, request: IRequest[Request]) -> IResponse[Request, Response]:
        raise NotImplementedError

    async def __aenter__(self: T) -> T:
        raise NotImplementedError

    async def __aexit__(self, cls: type[BaseException], *args: Any) -> bool | None:
        raise NotImplementedError

    def _inject_client(self, resource: pydantic.BaseModel):
        # Traverse the object hierarchy and add the client to each implementation
        # of IResource.
        resource._client = self
        for attname, field in resource.__fields__.items():
            if not inspect.isclass(field.type_)\
            or not issubclass(field.type_, IResource):
                continue
            value = getattr(resource, attname)
            if isinstance(value, Iterable):
                if isinstance(value, Mapping):
                    value = list(value.values())
                for subresource in value:
                    self._inject_client(subresource)

    async def _request_factory(self, *args: Any, **kwargs: Any) -> IRequest[Request]:
        request = await self.request_factory(*args, **kwargs)
        return self.request_class.fromimpl(request)

    async def listall(
        self,
        model: type[M],
        *params: Any,
        url: str | None = None
    ) -> Generator[M, None, None]:
        """Like :meth:`list()`, but returns all entities."""
        response = await self.request(
            method='GET',
            url=url or model.get_list_url(*params)
        )
        response.raise_for_status()
        self.check_json(response.headers)
        data = self.process_response('list', await response.json())
        data = model.process_response('list', data)
        resources = [
            self.resource_factory(model, None, x)
            for x in data
        ]
        while resources:
            yield resources.pop(0)
        url = model.get_next_url(response)
        if url is None:
            return
        async for resource in self.listall(model, *params, url=url):
            yield resource

    async def list(self, model: type[M]) -> Generator[M, None, None]:
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
        data = model.process_response('list', data)
        resources = [
            self.resource_factory(model, None, x)
            for x in data
        ]
        for resource in resources:
            yield resource