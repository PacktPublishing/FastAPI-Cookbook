from fastapi import (
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.security import OAuth2PasswordBearer


class OAuth2WebSocketPasswordBearer(
    OAuth2PasswordBearer
):
    async def __call__(
        self, websocket: WebSocket
    ) -> str:
        authorization: str = websocket.headers.get(
            "authorization"
        )
        if not authorization:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Not authenticated",
            )
        scheme, param = authorization.split()
        if scheme.lower() != "bearer":
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid authentication credentials",
            )
        return param
