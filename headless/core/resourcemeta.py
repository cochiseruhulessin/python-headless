# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any


class ResourceMeta:
    __module__: str = 'headless.core'
    base_endpoint: str

    @classmethod
    def frominnermeta(cls, meta: type) -> 'ResourceMeta':
        params: dict[str, Any] = {}
        params['base_endpoint'] = base_endpoint = getattr(meta, 'base_endpoint', None)
        if base_endpoint is None:
            raise TypeError(f'{meta.__name__}.base_endpoint is not defined.')
        if not str.startswith(base_endpoint, '/'):
            raise ValueError(f'{meta.__name__}.base_endpoint must start with a slash')
        if str.endswith(base_endpoint, '/'):
            raise ValueError(f'{meta.__name__}.base_endpoint must not end with a slash')
        return cls(**params)

    def __init__(
        self,
        base_endpoint: str
    ):
        self.base_endpoint = base_endpoint

    def get_retrieve_url(self, resource_id: int | str) -> str:
        """Return the URL to retrieve a single instance of the
        resource. This is a relative URL to the API base endpoint
        that is configured with a client instance.
        """
        return f'{self.base_endpoint}/{resource_id}'

    def get_list_url(self) -> str:
        """Return the URL to retrieve a list of instances of the
        resource. This is a relative URL to the API base endpoint
        that is configured with a client instance.
        """
        return self.base_endpoint