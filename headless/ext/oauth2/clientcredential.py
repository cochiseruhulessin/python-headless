# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.types import ICredential

from .models import ClientAuthenticationMethod
from .server import Server


class ClientCredential(ICredential):
    client_id: str
    client_secret: str
    server: Server

    def __init__(
        self,
        server: Server,
        client_id: str,
        client_secret: str,
        using: ClientAuthenticationMethod | None = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.server = server
        self.using = using or ClientAuthenticationMethod.none

    async def preprocess_request( # type: ignore
        self,
        url: str,
        json: dict[str, str],
        **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        if url != self.server.token_endpoint:
            return {**kwargs, 'url': url, 'json': json}
        if self.using == ClientAuthenticationMethod.client_secret_post:
            assert isinstance(json, dict)
            json.update({
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        else:
            raise NotImplementedError
        return {**kwargs, 'url': url, 'json': json}