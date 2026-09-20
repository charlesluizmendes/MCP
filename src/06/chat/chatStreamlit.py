import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from client.util.mcpClientUtil import McpClientUtil
from settings import get_client_id, get_client_secret, get_issuer, get_mcp_url
from llm.util.mcpLLmUtil import McpLLmUtil


st.title("NovaDrive — chat de exemplo")
st.caption("Consulte os dados da NovaDrive no PostgreSQL por meio do MCP.")

try:
    client_secret = get_client_secret()
except ValueError as error:
    st.error(str(error))
    st.stop()

if not os.getenv("OPENAI_API_KEY"):
    st.error("Configure OPENAI_API_KEY no ambiente para usar o chat.")
    st.stop()

if "llmClient" not in st.session_state:
    st.session_state.llmClient = McpLLmUtil(os.environ["OPENAI_MODEL"])
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


async def resolve_chat(message: str):
    client = McpClientUtil()
    async with client.initialize_with_http(
        get_mcp_url(), get_issuer(), get_client_id(), client_secret,
    ) as server:
        return await st.session_state.llmClient.complete_chat(message, server)


def run_async(coroutine):
    """Executa as chamadas assíncronas no mesmo loop durante a sessão."""
    loop = st.session_state.get("async_loop")
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        st.session_state.async_loop = loop
    return loop.run_until_complete(coroutine)


if prompt := st.chat_input("Quais veículos estão disponíveis?"):
    with st.chat_message("user"):
        st.write(prompt)
    try:
        with st.spinner("Consultando..."):
            answer = run_async(resolve_chat(prompt))
    except Exception as error:
        st.error(
            "Não foi possível responder. Confira se o MCP e o Keycloak estão ativos, "
            "se as credenciais OAuth estão corretas e se a chave OpenAI é válida. "
            "Você pode enviar a pergunta novamente."
        )
        with st.expander("Detalhes técnicos"):
            st.exception(error)
    else:
        st.session_state.messages.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ])
        st.rerun()

if st.session_state.llmClient.current_agent:
    st.toast(f"Agente atual: {st.session_state.llmClient.current_agent.name}")
