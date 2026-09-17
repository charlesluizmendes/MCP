from contextlib import asynccontextmanager

from agents.mcp import MCPServerStdio


class McpClientUtil:
    """Gerencia a conexão MCP utilizada pelos agentes de atendimento."""

    @asynccontextmanager
    async def initialize_with_stdio(self, command: str, args: list[str]):
        # Conexão e encerramento acontecem na mesma tarefa assíncrona.
        async with MCPServerStdio(params={"command": command, "args": args}) as server:
            yield server
