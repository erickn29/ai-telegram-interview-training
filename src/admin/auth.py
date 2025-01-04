# from sqladmin.authentication import AuthenticationBackend
# from starlette.requests import Request
#
# from core.config import config
# from core.database import db_conn
# from service.user import UserService
#
#
# class AdminAuth(AuthenticationBackend):
#     def __init__(self, secret_key: str) -> None:
#         super().__init__(secret_key)
#
#     async def login(self, request: Request) -> bool:
#         form = await request.form()
#         username, password = form["username"], form["password"]
#         session_generator = db_conn.get_session()
#         session = await anext(session_generator)
#         async with session:
#             auth_service = auth(session=session)
#             token = await auth_service.login(username, password)
#         if not token:
#             return False
#
#         request.session["token"] = token.refresh_token
#         return True
#
#     async def logout(self, request: Request) -> bool:
#         if not request.session.get("token"):
#             return False
#
#         del request.session["token"]  # TODO удаляются все куки решить!
#         return True
#
#     async def authenticate(self, request: Request) -> bool:
#         refresh_token = request.session.get("token")
#         if not refresh_token:
#             return False
#
#
# authentication_backend = AdminAuth(secret_key=config.app.secret_key)
