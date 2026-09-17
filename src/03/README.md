## O que é o projeto

Chat no terminal com um agente do SDK OpenAI Agents conectado a um servidor MCP via entrada e saída padrão (stdio). Permite consultar um banco PostgreSQL em linguagem natural, usando ferramentas para consultar tabelas e colunas, verificar a conexão e executar consultas SQL. Mantém o histórico da conversa.

## Execução

Na raiz do repositório, com o ambiente virtual ativo e a chave `OPENAI_API_KEY` configurada no `.env`, execute o chat. O servidor MCP é iniciado automaticamente; as consultas dependem do acesso ao PostgreSQL configurado no servidor.

```bash
python3 src/03/chat/chatAgent.py
```

Digite `sair`, `exit` ou `quit` para encerrar.
