from agents import Agent, ModelSettings, Runner


class McpLLmUtil:
    """Mantém os agentes, o histórico e o fluxo de atendimento."""

    def __init__(self, model: str):
        self.model = model
        self.history = []

        settings = ModelSettings(
            tool_choice="auto", temperature=0, parallel_tool_calls=False
        )

        self.agenteManutencao = Agent(
            name="ManutencaoAssistente",
            model=self.model,
            handoff_description="Assistente de manutenção e revisão para clientes que já possuem veículo.",
            instructions=(
                "Você é o assistente de manutenção da NovaDrive Motors. "
                "Ajude clientes que já possuem um veículo a agendar manutenção ou revisão. "
                "Peça o nome completo, use get_info_cliente para identificar os veículos "
                "e depois use agenda_visita_para_assistencia."
            ),
            model_settings=settings,
        )

        self.agentVendas = Agent(
            name="VendasAssistente",
            model=self.model,
            handoff_description="Assistente de vendas, veículos e agendamento de test drive.",
            instructions=(
                "Você é o assistente de vendas da NovaDrive Motors. "
                "Use get_veiculos_disponiveis para apresentar as opções. "
                "Quando o cliente quiser visitar uma concessionária, use "
                "get_concessionarias, get_vendedores_por_concessionaria e "
                "agenda_visita_para_compra. Não invente dados."
            ),
            model_settings=settings,
        )

        self.agentRecepcao = Agent(
            name="RecepcaoAssistente",
            model=self.model,
            handoffs=[self.agentVendas, self.agenteManutencao],
            instructions=(
                "Você é o assistente de recepção da NovaDrive Motors, empresa brasileira "
                "de veículos. Apresente a empresa e ofereça ajuda com compra, veículos, "
                "test drive, manutenção ou revisão. Encaminhe para vendas ou manutenção "
                "quando a intenção do cliente estiver clara."
            ),
            model_settings=settings,
        )

        self.current_agent = self.agentRecepcao

    async def complete_chat(self, message: str, server):
        self.history.append({"role": "user", "content": message})
        try:
            self.agentVendas.mcp_servers = [server]
            self.agenteManutencao.mcp_servers = [server]

            result = await Runner.run(
                starting_agent=self.current_agent,
                input=self.history,
                context=self.history,
            )
            self.current_agent = result.last_agent
            self.history = result.to_input_list()
            return result.final_output
        finally:
            self.agentVendas.mcp_servers = []
            self.agenteManutencao.mcp_servers = []
