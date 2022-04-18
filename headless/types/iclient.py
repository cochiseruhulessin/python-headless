"""Declares :class:`IClient`."""
from ckms.jose.models import JSONWebKeySet

from .capabilitytype import CapabilityType
from .icredential import ICredential


class IClient:
    """The base interface of all headless client implementations."""
    __module__: str = 'headless.types'
    capabilities: list[CapabilityType]
    server: str
    credential: ICredential
    version: str | None

    def __init__(
        self,
        server: str,
        credential: ICredential,
        version: str | None = None,
        capabilities: list[CapabilityType] = []
    ):
        self.capabilities = list(capabilities)
        self.server = server
        self.credential = credential
        self.version = version

    async def discover(self) -> None:
        pass

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