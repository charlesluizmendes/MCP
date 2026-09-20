"""Autenticação OAuth do cliente MCP."""

from mcp.client.auth.extensions.client_credentials import ClientCredentialsOAuthProvider
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from settings import get_required_scope


class MemoryTokenStorage:
    """Armazena o token somente durante a execução do cliente."""

    def __init__(self):
        self.tokens: OAuthToken | None = None
        self.client_info: OAuthClientInformationFull | None = None

    async def get_tokens(self):
        return self.tokens

    async def set_tokens(self, tokens):
        self.tokens = tokens

    async def get_client_info(self):
        return self.client_info

    async def set_client_info(self, client_info):
        self.client_info = client_info


def create_oauth_provider(url: str, issuer: str, client_id: str, client_secret: str):
    return ClientCredentialsOAuthProvider(
        server_url=url,
        issuer=issuer,
        storage=MemoryTokenStorage(),
        client_id=client_id,
        client_secret=client_secret,
        scopes=get_required_scope(),
    )
