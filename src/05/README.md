## O que é o projeto

Chat web em Streamlit para atendimento da NovaDrive Motors com três agentes do SDK OpenAI Agents: recepção, vendas e manutenção. A recepção encaminha o atendimento aos agentes especializados, que usam ferramentas MCP para consultar veículos, concessionárias, vendedores e clientes no PostgreSQL. Os agendamentos de visitas para compra e assistência são simulados, sem gravação no banco.

## Ferramentas por agente

As tools são atribuídas diretamente a cada agente em `McpLLmUtil.complete_chat`:

- **Recepção:** não recebe tools MCP; encaminha para os especialistas.
- **Vendas:** `get_veiculos_disponiveis`, `get_concessionarias`, `get_vendedores_por_concessionaria` e `agenda_visita_para_compra`.
- **Manutenção:** `get_info_cliente` e `agenda_visita_para_assistencia`.

A cada mensagem, as tools são convertidas pelo SDK e somente as permitidas são atribuídas a cada agente. Elas continuam sendo executadas pela mesma conexão MCP e são removidas dos agentes ao terminar a execução, inclusive em caso de erro. Novas tools do servidor precisam ser incluídas explicitamente nessa configuração para ficarem disponíveis.

## Execução

Na raiz do repositório, com o ambiente virtual ativo e a chave `OPENAI_API_KEY` configurada no `.env`, execute o aplicativo. O servidor MCP é iniciado automaticamente via stdio durante o atendimento; as consultas dependem do acesso ao PostgreSQL configurado nas variáveis `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD` do `.env`.

```bash
python3 -m streamlit run src/05/chat/chatStreamlit.py
```
