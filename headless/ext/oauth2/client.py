# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import Iterable
from typing import NoReturn

from headless.core import httpx
from headless.types import IResponse
from .clientcredential import ClientCredential
from .models import AuthorizationCode
from .models import ClientAuthenticationMethod
from .models import TokenResponse
from .server import Server


class Client(httpx.Client):
    """A :class:`headless.core.httpx.Client` implementation for use with
    Open Authorization/OpenID Connect servers.
    """
    __module__: str = 'headless.ext.oauth2'
    client_id: str
    credential: ClientCredential

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        issuer: str | None = None,
        client_auth: ClientAuthenticationMethod | None = None,
        authorization_endpoint: str | None = None,
        token_endpoint: str | None = None,
        **kwargs: Any
    ):
        self.server = Server(
            client=self,
            autodiscover=bool(issuer),
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            **kwargs
        )
        super().__init__(
            base_url=issuer or '',
            credential=ClientCredential(
                server=self.server,
                client_id=client_id,
                client_secret=client_secret,
                using=client_auth
            ),
        )

    async def authorize(
        self,
        state: str,
        redirect_uri: str | None,
        scope: Iterable[str] | None = None
    ) -> str:
        """Create an authorization request and return the URI to which
        the resource owner must be redirected.

        The `state` parameter is mandatory and is used to correlate the
        redirect to a specific authorization request.

        The `redirect_uri` parameter *might* be optional depending on the
        OAuth 2.x server. If the server does not allow omitting the
        `redirect_uri` parameter, this argument is mandatory.
        """
        params: dict[str, str] = {
            'client_id': self.credential.client_id,
            'state': state,
            'response_type': 'code',
        }
        if redirect_uri is not None:
            params['redirect_uri'] = redirect_uri
        if scope is not None:
            params['scope'] = str.join(' ', sorted(scope))
        response = await self.get(
            url=self.server.authorization_endpoint,
            params=params
        )
        if not 300 <= response.status_code <= 400:
            await self.on_authorize_endpoint_error(response)
        return response.headers['Location']

    @functools.singledispatchmethod
    async def token(
        self,
        obj: Any,
        **kwargs: Any
    ) -> TokenResponse:
        """Obtain an access token using the given grant."""
        raise NotImplementedError

    @token.register
    async def exchange_authorization_code(
        self,
        dto: AuthorizationCode,
        redirect_uri: str
    ) -> TokenResponse:
        params: dict[str, str] = {
            'client_id': self.credential.client_id,
            'code': dto.code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        response = await self.post(
            url=self.server.token_endpoint,
            json=params
        )
        response.raise_for_status()
        return TokenResponse.parse_obj(await response.json())

    async def on_authorize_endpoint_error(
        self,
        response: IResponse[Any, Any]
    ) -> NoReturn:
        response.raise_for_status()
        raise NotImplementedError