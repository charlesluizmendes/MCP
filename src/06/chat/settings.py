"""Configuração exclusiva do processo de chat e do cliente OAuth."""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[3] / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")


def get_client_secret() -> str:
    secret = os.getenv("OAUTH_CLIENT_SECRET", "")
    if not secret:
        raise ValueError("Configure OAUTH_CLIENT_SECRET no ambiente antes de iniciar o chat.")
    return secret


def get_mcp_url() -> str:
    return os.environ["MCP_SERVER_URL"]


def get_issuer() -> str:
    return os.environ["OAUTH_ISSUER"]


def get_client_id() -> str:
    return os.environ["OAUTH_CLIENT_ID"]


def get_required_scope() -> str:
    return os.environ["MCP_REQUIRED_SCOPE"]
