"""Declares :class:`JWTBearerCredential`."""
import typing

import ckms

from headless.types import ICredential


class JWTBearerCredential(ICredential):
    """A :class:`ICredential` implementation that obtains an access token "
    "using a `urn:ietf:params:oauth:grant-type:jwt-bearer` grant.
    """
    __module__: str = 'headless.credentials'
    audience: str
    keychain: ckms.Keychain
    scope: set[str]
    server: str
    subject: str

    def __init__(
        self,
        server: str,
        subject: str,
        scope: set[str],
        keyspec: dict[str, typing.Any],
        audience: str | None = None
    ):
        self.audience = audience or server
        self.keyhain = ckms.Keychain()
        self.scope = scope
        self.server = server
        self.subject = subject

        self.keychain.register(keyspec)