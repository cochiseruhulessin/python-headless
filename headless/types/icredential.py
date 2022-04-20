"""Declares :class:`ICredential`."""
from .irequest import IRequest


class ICredential:
    """The base class for all credential implementations. A credential
    provides a means for the client to obtain an access token which
    grants access to protected resources.
    """
    __module__: str = 'headless.types'

    async def authenticate(self, request: IRequest) -> None:
        """Authenticates a request, for example by setting the
        ``Authorization`` header or a session cookie.
        """
        raise NotImplementedError