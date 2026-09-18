from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPUtil


class McpLLmUtil:
    """Mantém os agentes, o histórico e o fluxo de atendimento."""

    def __init__(self, model: str):
        self.model = model
        self.history = []

        settings = ModelSettings(tool_choice="auto", temperature=0, parallel_tool_calls=False)

        self.agenteManutencao = Agent(
            name="ManutencaoAssistente",
            model=self.model,
            handoff_description="Assistente de manutenção/revisão para clientes que já possuem veículo/carro.",
            instructions=(
                "Você é um assistente da NovaDrive Motors que deve ajudar o cliente a agendar uma visita para manutenção ou revisão."
                "Pergunte o nome completo para identificar o cliente e então use as ferramentas para descobrir os veículos/carros que tem (get_info_cliente). "
                "Com base nisso colete as informações do que ele precisa, agende um horário na concessionária onde comprou o veículo (com agenda_visita_para_assistencia)."
                "Não é necessario escolher um vendedor, apenas agendar a visita na concessionária onde comprou o veículo/carro. "
            ),
            model_settings=settings,
        )

        self.agentVendas = Agent(
            name="VendasAssistente",
            model=self.model,
            handoff_description="Assistente para trativa de vendas, informações sobre veículos e agendamento de visitas/test drive.",
            instructions=(
                "Você é um assistente da NovaDrive Motors que deve ajudar e convencer o cliente a comprar um carro/veículo."
                "Antes de tudo use a ferramenta get_veiculos_disponiveis para conhecer as opções disponíveis e apresentar a ele. "
                "Você pode fazer perguntas para entender o que o cliente precisa e oferecer as melhores opções de veículos/carros baseado na ferramenta que você chamou. "
                "Quando o cliente decidir, agende uma visita na concessionária mais próxima do cliente, para descobrir as concessionárias use get_concessionarias "
                "e para descobrir os vendedores dessa concessionária use get_vendedores_por_concessionaria. "
                "Então, agende a visita com a ferramenta agenda_visita_para_compra, onde você vai escolher o vendedor e a concessionária mais próxima do cliente."
            ),
            model_settings=settings,
        )

        self.agentRecepcao = Agent(
            name="RecepcaoAssistente",
            model=self.model,
            handoffs=[self.agentVendas, self.agenteManutencao],
            instructions=(
                "Você é um assistente de recepção da NovaDrive Motors, uma empresa nacional de veículos/carros do Brasil."
                "Você é responsável pela recepção e deve apenas apresentar a empresa e oferecer as opções disponíveis. "
                "Apresente a NovaDrive Motors como empresa de veículos/carros e orgulhosamente brasileira."
                "Mostre o site https://www.novadrivemotors.com.br/ para conhecer mais sobre a empresa."
                "Ofereça para conhecer os carros e agendar uma visita com vendedor com possibilidade de test drive."
                "Ou então no caso de querer manutenção ou revisão pode agendar uma visita a concessionária."
            ),
            model_settings=settings,
        )

        self.current_agent = self.agentRecepcao

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    async def complete_chat(self, server):
        tools_mcp = await MCPUtil.get_function_tools(server, convert_schemas_to_strict=False)
        tools = {tool.name: tool for tool in tools_mcp}
        try:
            self.agentVendas.tools = [
                tools["get_veiculos_disponiveis"],
                tools["get_concessionarias"],
                tools["get_vendedores_por_concessionaria"],
                tools["agenda_visita_para_compra"],
            ]
            self.agenteManutencao.tools = [
                tools["get_info_cliente"],
                tools["agenda_visita_para_assistencia"],
            ]

            result = await Runner.run(
                starting_agent=self.current_agent,
                input=self.history,
                context=self.history,
            )
            self.current_agent = result.last_agent
            self.history = result.to_input_list()
            return result
        finally:
            # As tools guardam a conexão, que será encerrada ao sair do atendimento.
            self.agentVendas.tools = []
            self.agenteManutencao.tools = []
