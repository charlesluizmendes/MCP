import asyncio, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.mcpClientUtil import McpUClienttil


async def main():
    mcpClientUtil = McpUClienttil()

    try:
        # await mcpUtil.initialize_with_stdio("mcp", ["run", "src/02/server/server.py"])
        
        # caso queira conectar por sse
        await mcpClientUtil.initialize_with_sse("http://localhost:8000/sse")

        print("Listando tools")
        tools = await mcpClientUtil.get_tools()
        for tool in tools:
            print(f'Nome: {tool.name}, Descrição: {tool.description}')

            if tool.name == 'adiciona':
                print("Chamando a ferramenta adiciona")
                result = await mcpClientUtil.call_tool("adiciona", {"a": 1, "b": 20})
                print(result.content[0].text)

        print("\nListando resources")
        resources = await mcpClientUtil.get_resources()
        for resource in resources:
            print(resource)

            if resource.mimeType == 'text/plain':
                print(f"Acessando recurso {resource.name}")
                result = await mcpClientUtil.get_resource(resource.uri)
                print(result.contents[0].text)

        print("\nListando prompts")
        prompts = await mcpClientUtil.get_prompts()
        for prompt in prompts:
            print(prompt)

            if prompt.name == 'formatar_dado_cadastral':
                print("Formatando Dado Cadastral")
                result = await mcpClientUtil.invoke_prompt(prompt.name, {"cpf": "12312312312"})
                print(result.messages[0].content.text)
    finally:
        await mcpClientUtil.cleanup()

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    asyncio.run(main())
