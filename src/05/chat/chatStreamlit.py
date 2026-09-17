from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPServerStdio 
import streamlit as st
from dotenv import load_dotenv
import asyncio, json, sys, os

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.markdown("<h1 style='text-align: center;'>NovoDrive Motors</h1>", unsafe_allow_html=True)

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "novadrive.png")
    st.image(image_path, caption="NovaDrive Motors")

if "history" not in st.session_state:
    load_dotenv()  
    st.session_state.history = []

for message in st.session_state.history:
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
        
if "agentRecepcao" not in st.session_state: 
        agenteManutencao = Agent( 
            name="ManutencaoAssistente", 
            model="gpt-4.1-mini",
            handoff_description="Assistente de manutenção/revisão para clientes que já possuem veículo/carro.",
            instructions="Você é um assistente da NovaDrive Motors que deve ajudar o cliente a agendar uma visita para manutenção ou revisão." \
                "Pergunte o nome completo para identificar o cliente e então use as ferramentas para descobrir os veículos/carros que tem (get_info_cliente). " \
                "Com base nisso colete as informações do que ele precisa, agende um horário na concessionária onde comprou o veículo (com agenda_visita_para_assistencia)." \
                "Não é necessario escolher um vendedor, apenas agendar a visita na concessionária onde comprou o veículo/carro. ",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        agentVendas = Agent(  
            name="VendasAssistente", 
            model="gpt-4.1-mini",
            handoff_description="Assistente para trativa de vendas, informações sobre veículos e agendamento de visitas/test drive.",
            instructions="Você é um assistente da NovaDrive Motors que deve ajudar e convencer o cliente a comprar um carro/veículo." \
                "Antes de tudo use a ferramenta get_veiculos_disponiveis para conhecer as opções disponíveis e apresentar a ele. " \
                "Você pode fazer perguntas para entender o que o cliente precisa e oferecer as melhores opções de veículos/carros baseado na ferramenta que você chamou. " \
                "Quando o cliente decidir, agende uma visita na concessionária mais próxima do cliente, para descobrir as concessionárias use get_concessionarias " \
                "e para descobrir os vendedores dessa concessionária use get_vendedores_por_concessionaria. " \
                "Então, agende a visita com a ferramenta agenda_visita_para_compra, onde você vai escolher o vendedor e a concessionária mais próxima do cliente.",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        agentRecepcao = Agent( 
            name="RecepcaoAssistente", 
            model="gpt-4.1-mini",
            handoffs=[agentVendas, agenteManutencao], 
            instructions="Você é um assistente de recepção da NovaDrive Motors, uma empresa nacional de veículos/carros do Brasil." \
                "Você é responsável pela recepção e deve apenas apresentar a empresa e oferecer as opções disponíveis. " \
                "Apresente a NovaDrive Motors como empresa de veículos/carros e orgulhosamente brasileira." \
                "Mostre o site https://www.novadrivemotors.com.br/ para conhecer mais sobre a empresa." \
                "Ofereça para conhecer os carros e agendar uma visita com vendedor com possibilidade de test drive." \
                "Ou então no caso de querer manutenção ou revisão pode agendar uma visita a concessionária.",
            model_settings=ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False), 
        )

        st.session_state.agentRecepcao = agentRecepcao
        st.session_state.agentVendas = agentVendas
        st.session_state.agenteManutencao = agenteManutencao
        st.session_state.current_agent = agentRecepcao 

async def resolve_chat(): 
    async with MCPServerStdio(params={"command": "mcp", "args": ["run", "src/05/server/mcpServerSql.py"]}) as server:
        st.session_state.agentVendas.mcp_servers = [server] 
        st.session_state.agenteManutencao.mcp_servers = [server] 

        result = await Runner.run(
            starting_agent=st.session_state.current_agent, 
            input=st.session_state.history, 
            context=st.session_state.history
        )
       
        st.session_state.current_agent = result.last_agent
        st.session_state.history = result.to_input_list()
      
prompt = st.chat_input("Digite sua pergunta:")

if prompt:
    st.session_state.history.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Pensando..."):
        asyncio.run(resolve_chat())
        st.rerun()

if "current_agent" in st.session_state: 
    st.toast(f"Agente atual: { st.session_state.current_agent.name }")
