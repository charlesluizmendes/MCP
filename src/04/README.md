## O que é o projeto

Chat web em Streamlit para consultar o banco PostgreSQL da NovaDrive Motors em linguagem natural. Integra a API de chat da OpenAI a um cliente MCP próprio, que descobre e executa ferramentas para consultar tabelas e colunas, verificar a conexão e executar consultas SQL. A interface exibe o histórico, os argumentos e os resultados das chamadas de ferramentas.

## Execução

Na raiz do repositório, com o ambiente virtual ativo e a chave `OPENAI_API_KEY` configurada no `.env`, execute o aplicativo. O cliente inicia o servidor MCP automaticamente via stdio; as consultas dependem do acesso ao PostgreSQL configurado nas variáveis `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD` do `.env`.

```bash
python3 -m streamlit run src/04/chat/chatStreamlit.py
```
