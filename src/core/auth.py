import jwt

from core.config import config


class JWTAuthenticationBackend:
    def __init__(
        self,
        alg: str = "HS256",
        typ: str = "JWT",
    ):
        self.alg = alg
        self.typ = typ


token = jwt.encode(
    {"id": "123"},
    config.app.secret_key,
)

print(token)
print(
    jwt.decode(
        # token,
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMyJ9.lH9-eoStqfdjoyeZMGo09Ztjg4TFrV1xIUsDg98mtoo",
        config.app.secret_key,
        "HS256",
    )
)
