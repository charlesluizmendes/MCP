## O que é o projeto

Chat web em Streamlit para atendimento da NovaDrive Motors com três agentes do SDK OpenAI Agents: recepção, vendas e manutenção. A recepção encaminha o atendimento aos agentes especializados, que usam ferramentas MCP para consultar veículos, concessionárias, vendedores e clientes no PostgreSQL. Os agendamentos de visitas para compra e assistência são simulados, sem gravação no banco.

## Execução

Na raiz do repositório, com o ambiente virtual ativo e a chave `OPENAI_API_KEY` configurada no `.env`, execute o aplicativo. O servidor MCP é iniciado automaticamente via stdio durante o atendimento; as consultas dependem do acesso ao PostgreSQL configurado no servidor.

```bash
python3 -m streamlit run src/05/chat/chatStreamlit.py
```
