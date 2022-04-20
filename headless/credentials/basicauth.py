"""Declares :class:`BasicAuthCredential`."""
import base64

from headless.types import ICredential
from headless.types import IRequest


class BasicAuthCredential(ICredential):
    __module__: str = 'headless.types'
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    async def authenticate(self, request: IRequest) -> None:
        request.headers['Authorization'] = self._build_auth_header(
            username=self.username,
            password=self.password
        )

    def _build_auth_header(
        self,
        username: str,
        password: str
    ) -> str:
        credential = ":".join([username, password])
        token = base64.b64encode(str.encode(credential))
        return f"Basic {bytes.decode(token)}"