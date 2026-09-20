import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg2
from dotenv import load_dotenv
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl

from server.auth import KeycloakTokenVerifier

# O banco continua usando o .env geral dos projetos anteriores.
load_dotenv(Path(__file__).resolve().parents[3] / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}

MCP_SERVER_URL = os.environ["MCP_SERVER_URL"]
OAUTH_ISSUER = os.environ["OAUTH_ISSUER"]
REQUIRED_SCOPE = os.environ["MCP_REQUIRED_SCOPE"]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_app(issuer: str, resource_url: str):
    mcp = FastMCP(
        "NovaDrive — exemplo autenticado",
        host=os.environ["MCP_HOST"],
        stateless_http=True,
        json_response=True,
        token_verifier=KeycloakTokenVerifier(issuer, resource_url),
        auth=AuthSettings(
            issuer_url=AnyHttpUrl(issuer),
            resource_server_url=AnyHttpUrl(resource_url),
            required_scopes=[REQUIRED_SCOPE],
            validate_token_resource=True,
        ),
    )

    @mcp.tool()
    def get_veiculos_disponiveis():
        """Retorna os veículos/carros disponíveis para a compra."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("select nome, tipo, valor from veiculos v;")
                    rows = cursor.fetchall()
                    result = [
                        dict(zip([desc[0] for desc in cursor.description], row))
                        for row in rows
                    ]
            return json.dumps(result, indent=4, sort_keys=True, default=str)
        except Exception as error:
            return {"error": str(error)}

    @mcp.tool()
    def get_concessionarias():
        """Retorna as concessionárias e suas informações de localização."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        select c.id_concessionarias, c.concessionaria, c2.cidade,
                               e.estado, e.sigla
                        from concessionarias c
                        join cidades c2 on c2.id_cidades = c.id_cidades
                        join estados e on c2.id_estados = e.id_estados;
                    """)
                    rows = cursor.fetchall()
                    result = [
                        dict(zip([desc[0] for desc in cursor.description], row))
                        for row in rows
                    ]
            return json.dumps(result, indent=4, sort_keys=True, default=str)
        except Exception as error:
            return {"error": str(error)}

    @mcp.tool()
    def get_vendedores_por_concessionaria(id_concessionarias: int):
        """Retorna os vendedores por id de concessionária."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        select v.id_vendedores, v.nome
                        from vendedores v
                        where v.id_concessionarias = %s;
                    """, (id_concessionarias,))
                    rows = cursor.fetchall()
                    result = [
                        dict(zip([desc[0] for desc in cursor.description], row))
                        for row in rows
                    ]
            return json.dumps(result, indent=4, sort_keys=True, default=str)
        except Exception as error:
            return {"error": str(error)}

    @mcp.tool()
    def get_info_cliente(nome: str):
        """Retorna dados do cliente e os veículos comprados."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        select c.id_clientes, c.cliente, c2.concessionaria,
                               c3.cidade, e.estado, v.data_venda, v.valor_pago,
                               v2.nome as carro
                        from clientes c
                        join concessionarias c2 on c.id_concessionarias = c2.id_concessionarias
                        join cidades c3 on c3.id_cidades = c2.id_cidades
                        join estados e on e.id_estados = c3.id_estados
                        join vendas v on v.id_clientes = c.id_clientes
                        join veiculos v2 on v2.id_veiculos = v.id_veiculos
                        where c.cliente = %s;
                    """, (nome,))
                    rows = cursor.fetchall()
                    result = [
                        dict(zip([desc[0] for desc in cursor.description], row))
                        for row in rows
                    ]
            return json.dumps(result, indent=4, sort_keys=True, default=str)
        except Exception as error:
            return {"error": str(error)}

    @mcp.tool()
    def agenda_visita_para_compra(
        id_concessionaria: int, id_vendedor: int, data_hora: str
    ):
        """Agenda uma visita de compra; neste exemplo, a operação é simulada."""
        return {"message": "Visita agendada com sucesso!"}

    @mcp.tool()
    def agenda_visita_para_assistencia(
        id_cliente: int,
        id_concessionaria: int,
        nome_carro: str,
        detalhes: str,
        data_hora: str,
    ):
        """Agenda uma visita de assistência; neste exemplo, a operação é simulada."""
        return {"message": "Visita de manutenção/revisão agendada com sucesso!"}

    # O SDK publica os metadados OAuth e protege /mcp com validação de token e scope.
    return mcp.streamable_http_app()


if __name__ == "__main__":
    app = create_app(OAUTH_ISSUER, MCP_SERVER_URL)
    uvicorn.run(
        app,
        host=os.environ["MCP_HOST"],
        port=int(os.environ["MCP_PORT"]),
        timeout_graceful_shutdown=5,
    )
