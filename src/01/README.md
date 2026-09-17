## O que é o projeto

Servidor MCP (Model Context Protocol) de exemplo para um assistente financeiro. Disponibiliza uma ferramenta para somar dois números, um recurso para ler despesas mensais do arquivo `resource/contas.txt` e um prompt para formatar CPF.

## Execução

Na raiz do repositório, com o ambiente virtual ativo, execute apenas o servidor via SSE:

```bash
mcp run src/01/server/mcpServer.py --transport sse
```

Ou execute em modo de desenvolvimento, com o MCP Inspector para testar ferramentas, recursos e prompts:

```bash
mcp dev src/01/server/mcpServer.py
```
