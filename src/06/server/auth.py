"""Valida access tokens do Keycloak; este servidor não emite tokens."""

import asyncio

import jwt
from mcp.server.auth.provider import AccessToken, TokenVerifier


class KeycloakTokenVerifier(TokenVerifier):
    def __init__(self, issuer: str, audience: str):
        self.issuer = issuer
        self.audience = audience
        # Chaves públicas do emissor confiável, nunca de uma URL fornecida pelo token.
        self.jwks = jwt.PyJWKClient(
            f"{issuer}/protocol/openid-connect/certs", timeout=5, lifespan=300,
        )

    async def verify_token(self, token: str) -> AccessToken | None:
        # PyJWKClient faz I/O síncrono; a thread não bloqueia o servidor assíncrono.
        return await asyncio.to_thread(self._verify, token)

    def _verify(self, token: str) -> AccessToken | None:
        try:
            key = self.jwks.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience,
                options={"require": ["exp", "iat", "iss", "aud", "sub", "azp"]},
            )
            return AccessToken(
                token=token,
                client_id=claims["azp"],
                subject=claims["sub"],
                scopes=claims.get("scope", "").split(),
                expires_at=claims["exp"],
                resource=self.audience,
                claims={"iss": claims["iss"]},
            )
        except (jwt.PyJWTError, ValueError, TypeError, AttributeError):
            # Não registra o token nem expõe detalhes da validação ao cliente.
            return None
