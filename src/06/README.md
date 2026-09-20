## O que é o projeto

Chat web em Streamlit com um agente do SDK OpenAI Agents que consulta ferramentas MCP por Streamable HTTP. O projeto demonstra autenticação OAuth Client Credentials entre três ambientes separados: chat, servidor MCP e Keycloak. O servidor usa as mesmas ferramentas e o mesmo PostgreSQL do projeto 05.

O chat obtém um JWT no Keycloak e o envia ao servidor MCP. O servidor valida assinatura, emissor, validade, audience e escopo antes de executar uma ferramenta.

## Componentes

- **Chat:** interface Streamlit, agente LLM e cliente MCP em `src/06/chat`.
- **Servidor:** FastMCP, ferramentas e validação dos JWTs em `src/06/server`.
- **Keycloak:** provedor OAuth, Compose e configuração do realm em `src/06/keycloak`.

O arquivo `novadrive-realm.json` configura automaticamente o realm `novadrive`, o cliente OAuth, o escopo `novadrive:read` e a audience do MCP. Ele não é uma API nem guarda os segredos.

## Execução

Na raiz do repositório, use a virtualenv global e o `requirements.txt` geral:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

Cada ambiente tem seu próprio `.env`:

```text
src/06/chat/.env       # credenciais do chat e cliente OAuth
src/06/server/.env     # endereço e proteção do MCP
src/06/keycloak/.env   # senha administrativa e segredo do cliente
```

As configurações `OPENAI_API_KEY`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e
`DB_PASSWORD` continuam no `.env` da raiz, como nos projetos anteriores. O
chat e o servidor 06 carregam esse arquivo; as configurações OAuth ficam nos
`.env` de `chat`, `server` e `keycloak`.

Preencha os valores dos arquivos antes de iniciar. O
`OAUTH_CLIENT_SECRET` deve ser igual nos arquivos `chat/.env` e
`keycloak/.env`. Em produção, injete os valores por um gerenciador de
segredos. Gere um segredo com `python -c "import secrets; print(secrets.token_urlsafe(32))"`.

Os `.env` do projeto 06 são versionados apenas para manter este exemplo
simples. Em produção, injete os valores por um gerenciador de segredos.

Em um terminal, inicie o Keycloak:

```bash
docker compose --env-file src/06/keycloak/.env -f src/06/keycloak/compose.yaml up -d
```

Em outro terminal, inicie o servidor MCP:

```bash
python src/06/server/mcpServer.py
```

Em outro terminal, inicie o chat:

```bash
python -m streamlit run src/06/chat/chatStreamlit.py
```

O exemplo autentica a aplicação do chat. Não há login individual de usuário; para esse cenário, o fluxo adequado é Authorization Code com PKCE.
