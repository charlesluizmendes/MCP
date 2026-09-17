import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv

from client.util.mcpClientUtil import McpClientUtil
from llm.util.mcpLLmUtil import McpLLmUtil


tool = "src/05/server/mcpServerSql.py"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.markdown("<h1 style='text-align: center;'>NovoDrive Motors</h1>", unsafe_allow_html=True)

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "novadrive.png")
    st.image(image_path, caption="NovaDrive Motors")

if "llmClient" not in st.session_state:
    load_dotenv()
    st.session_state.llmClient = McpLLmUtil("gpt-4.1-mini")

for message in st.session_state.llmClient.history:
    type = message.get("role", None) or message.get("type", None)

    match type:
        case 'user':
            with st.chat_message(type):
                st.markdown(message["content"])
        case 'assistant':
            with st.chat_message(type):
                st.markdown(message["content"][0]["text"])
        case 'function_call':
            if "transfer_to" not in message["name"]:
                with st.chat_message(name="tool", avatar=":material/build:"):
                        st.markdown(f'LLM chamando tool {message["name"]}')
                        with st.expander("Visualizar argumentos"):
                            st.code(message["arguments"])
        case 'function_call_output':
            try:
                obj = json.loads(message['output'])
                with st.chat_message(name="tool", avatar=":material/data_object:"):
                    with st.expander("Visualizar resposta"):
                        st.code(obj["text"])
            except:
                continue

async def resolve_chat():
    client = McpClientUtil()
    async with client.initialize_with_stdio("mcp", ["run", tool]) as server:
        await st.session_state.llmClient.complete_chat(server)


prompt = st.chat_input("Digite sua pergunta:")

if prompt:
    st.session_state.llmClient.add_user_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Pensando..."):
        asyncio.run(resolve_chat())
        st.rerun()

st.toast(f"Agente atual: {st.session_state.llmClient.current_agent.name}")
