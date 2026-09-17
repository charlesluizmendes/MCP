## O que é o projeto

Exemplo de comunicação entre um cliente Python e um servidor MCP de assistência financeira via SSE. O cliente lista e utiliza as ferramentas, os recursos e os prompts do servidor: soma dois números, lê as despesas de `resource/contas.txt` e obtém um prompt para formatar CPF.

## Execução

Na raiz do repositório, com o ambiente virtual ativo, inicie o servidor em um terminal:

```bash
mcp run src/02/server/mcpServer.py --transport sse
```

Em outro terminal, também na raiz e com o ambiente virtual ativo, execute o cliente:

```bash
python3 src/02/client/mcpClient.py
```
