from contextlib import asynccontextmanager

from agents.mcp import MCPServerStreamableHttp
from client.oauth import create_oauth_provider


class McpClientUtil:
    """Cliente MCP pertencente ao processo de chat."""

    @asynccontextmanager
    async def initialize_with_http(self, url: str, issuer: str, client_id: str, client_secret: str):
        oauth = create_oauth_provider(url, issuer, client_id, client_secret)
        async with MCPServerStreamableHttp(
            name="NovaDrive MCP",
            params={"url": url, "auth": oauth, "timeout": 15},
            cache_tools_list=True,
            client_session_timeout_seconds=15,
        ) as server:
            yield server
