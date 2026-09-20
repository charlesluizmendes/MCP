# Exemplos de MCP com Python

Repositório de exemplos de uso do **Model Context Protocol (MCP)** para conectar aplicações e agentes de inteligência artificial a ferramentas, recursos e prompts. Os seis projetos apresentam uma evolução: um servidor básico, um cliente Python, um chat no terminal, uma interface web, um atendimento com agentes especializados e um chat com MCP HTTP autenticado.

Os exemplos usam Python, FastMCP, PostgreSQL, Streamlit e integrações com a OpenAI, conforme a proposta de cada pasta.

## Projetos

| Pasta | Projeto | O que demonstra |
| --- | --- | --- |
| [01](src/01/README.md) | Servidor MCP básico | Assistente financeiro com ferramenta de soma, recurso de despesas em arquivo e prompt para formatação de CPF. |
| [02](src/02/README.md) | Cliente e servidor MCP | Cliente Python que se conecta ao servidor via SSE, lista e utiliza ferramentas, recursos e prompts. |
| [03](src/03/README.md) | Chat com banco de dados no terminal | Agente do SDK OpenAI Agents que usa um servidor MCP para consultar o esquema e os dados de um PostgreSQL. |
| [04](src/04/README.md) | Chat com banco de dados no navegador | Interface Streamlit com cliente MCP próprio e integração com a API de chat da OpenAI, exibindo chamadas de ferramentas e resultados. |
| [05](src/05/README.md) | Atendimento com múltiplos agentes | Interface Streamlit com agentes de recepção, vendas e manutenção da NovaDrive Motors, consultas ao PostgreSQL e agendamentos simulados. |
| [06](src/06/README.md) | Chat com MCP HTTP autenticado | Streamable HTTP com OAuth Client Credentials, Keycloak local, validação JWT e as ferramentas PostgreSQL do projeto 05. |

As pastas contêm exemplos independentes. A ordem de `01` a `06` ajuda a acompanhar a evolução das integrações.

## Estrutura

```text
MCP/
├── README.md
├── requirements.txt          # Dependências Python
└── src/
    ├── 01/
    │   ├── README.md
    │   ├── resource/         # Arquivo de despesas
    │   └── server/           # Servidor MCP financeiro
    ├── 02/
    │   ├── README.md
    │   ├── client/           # Cliente MCP e utilitários de conexão
    │   ├── resource/         # Arquivo de despesas
    │   └── server/           # Servidor MCP financeiro
    ├── 03/
    │   ├── README.md
    │   ├── chat/             # Chat no terminal
    │   └── server/           # Ferramentas MCP para PostgreSQL
    ├── 04/
    │   ├── README.md
    │   ├── chat/             # Interface Streamlit e imagem
    │   ├── client/           # Cliente MCP próprio
    │   ├── llm/              # Integração com o modelo de linguagem
    │   └── server/           # Ferramentas MCP para PostgreSQL
    ├── 05/
    │   ├── README.md
    │   ├── chat/             # Interface Streamlit e imagem
    │   ├── client/           # Conexão MCP para os agentes
    │   ├── llm/              # Agentes e histórico da conversa
    │   └── server/           # Ferramentas de atendimento da concessionária
    └── 06/
        ├── README.md
        ├── chat/            # Chat, cliente MCP, LLM e configuração do chat
        ├── server/          # FastMCP e validação JWT
        ├── keycloak/        # Compose, realm e cliente OAuth
```

## Preparação do ambiente

Todos os projetos usam o `requirements.txt` da raiz. O projeto 06 usa as variáveis de ambiente descritas em seu [README](src/06/README.md).

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows, a ativação pelo PowerShell é:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

Para os projetos `03`, `04` e `05`, configure a chave da OpenAI e a conexão PostgreSQL em um arquivo `.env` na raiz:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Esses projetos também precisam de acesso ao PostgreSQL utilizado pelos exemplos. Os três servidores carregam o `.env` da raiz, independentemente do diretório de execução. Variáveis já definidas no ambiente têm prioridade sobre o arquivo. O repositório não inclui scripts para criar ou popular o banco. No projeto `05`, as consultas dependem das tabelas de veículos, concessionárias, cidades, estados, vendedores, clientes e vendas.

## Execução

Mantenha o ambiente virtual ativo e execute os comandos na raiz do repositório.

### 01 — Servidor MCP básico

Inicie o servidor com transporte SSE:

```bash
mcp run src/01/server/mcpServer.py --transport sse
```

Como alternativa, use o modo de desenvolvimento com o MCP Inspector para explorar as ferramentas, os recursos e os prompts:

```bash
mcp dev src/01/server/mcpServer.py
```

### 02 — Cliente e servidor MCP

Em um terminal, inicie o servidor:

```bash
mcp run src/02/server/mcpServer.py --transport sse
```

Em outro terminal, com o ambiente virtual também ativo, execute o cliente. Ele se conecta a `http://localhost:8000/sse`:

```bash
python3 src/02/client/mcpClient.py
```

### 03 — Chat no terminal

```bash
python3 src/03/chat/chatAgent.py
```

Digite perguntas sobre o banco de dados. Para encerrar, digite `sair`, `exit` ou `quit`.

### 04 — Chat web com ferramentas SQL

```bash
python3 -m streamlit run src/04/chat/chatStreamlit.py
```

### 05 — Chat web com agentes de atendimento

```bash
python3 -m streamlit run src/05/chat/chatStreamlit.py
```

Nos projetos `04` e `05`, abra o endereço exibido pelo Streamlit no terminal. Use o comando `streamlit run` conforme os exemplos para inicializar a interface e o estado da sessão.

Os projetos `03`, `04` e `05` iniciam seus servidores MCP automaticamente por entrada e saída padrão (stdio).

### 06 — Chat com MCP HTTP autenticado

Após a [configuração do projeto 06](src/06/README.md), inicie o provedor OAuth local:

```bash
docker compose --env-file src/06/keycloak/.env -f src/06/keycloak/compose.yaml up -d
```

Com a `venv` da raiz ativa nos dois terminais, inicie o servidor em um deles:

```bash
python src/06/server/mcpServer.py
```

No outro, inicie o chat:

```bash
python -m streamlit run src/06/chat/chatStreamlit.py
```

O cliente descobre o Keycloak pelo MCP, obtém um token via OAuth Client Credentials e acessa `http://127.0.0.1:8006/mcp`. O servidor valida assinatura, expiração, emissor, destinatário e o escopo `novadrive:read` antes de permitir o acesso às ferramentas de atendimento e consultas PostgreSQL do projeto 05. O projeto 05 permanece em stdio.

## Como as integrações funcionam

Nos projetos `01` e `02`, o servidor expõe três elementos do MCP: uma **ferramenta** que executa uma soma, um **recurso** que fornece as despesas de um arquivo e um **prompt** que monta uma instrução para formatar CPF.

Nos projetos `03` e `04`, o modelo recebe a pergunta do usuário e pode chamar ferramentas MCP para descobrir tabelas e colunas, verificar a conexão e executar SQL. O resultado volta ao modelo para compor a resposta. O projeto `03` usa o SDK OpenAI Agents; o `04` implementa o fluxo de chamadas de ferramentas com utilitários próprios.

No projeto `05`, o agente de recepção encaminha a conversa para vendas ou manutenção. Os agentes especializados consultam ferramentas de negócio, como listar veículos e identificar clientes. As ferramentas de agendamento retornam mensagens de sucesso simuladas e não gravam visitas no banco.

No projeto `06`, o chat e o servidor MCP são processos separados e se comunicam por Streamable HTTP. O cliente do chat obtém um token OAuth Client Credentials no Keycloak e o envia ao MCP. O servidor valida o JWT, o escopo e a audience antes de executar as ferramentas de atendimento do projeto 05, usando o PostgreSQL configurado no `.env` da raiz.
