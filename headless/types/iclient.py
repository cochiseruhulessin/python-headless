"""Declares :class:`IClient`."""
import types
import typing

from ckms.jose.models import JSONWebKeySet

from .capabilitytype import CapabilityType
from .icredential import ICredential
from .iresponse import IResponse


class IClient:
    """The base interface of all headless client implementations."""
    __module__: str = 'headless.types'
    base_path: str  = '/'
    capabilities: list[CapabilityType]
    server: str
    credential: ICredential

    def __init__(
        self,
        server: str,
        credential: ICredential,
        base_path: str = '/',
        capabilities: list[CapabilityType] = []
    ):
        self.capabilities = list(capabilities)
        self.server = server
        self.credential = credential
        self.base_path = base_path

    async def discover(self) -> None:
        pass

    async def get(
        self,
        path: str,
        params: typing.Any = None
    ) -> IResponse:
        raise NotImplementedError

    async def put(
        self,
        path: str,
        params: typing.Any = None,
        json: dict[str, typing.Any] | None = None
    ) -> IResponse:
        raise NotImplementedError

    async def get_server_time(self) -> int:
        """Return an integer indicating the server time, in seconds since
        the UNIX epoch.
        """
        raise NotImplementedError

    async def get_server_jwks(self) -> JSONWebKeySet:
        """Lookup the JSON Web Key Set (JWKS) published by the
        remote peer to encrypt sent data and verify signatures
        created by it.
        """
        raise NotImplementedError

    async def __aexit__(
        self,
        cls: type[BaseException],
        exception: BaseException,
        traceback: types.TracebackType
    ) -> bool:
        raise NotImplementedError