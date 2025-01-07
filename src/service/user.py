from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import config
from core.database import db_conn
from model.user import User
from repository.question import QuestionRepository
from repository.user import UserRepository
from service.base import BaseService


PWD_CONTEXT = config.auth.pwd_context


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserRepository)

    async def find(self, **filters):
        return await self.repository.find(**filters)

    @staticmethod
    async def delete_user_cache(user_id: UUID):
        from core.cache import cache

        if await cache.get_user(str(user_id)):
            await cache.delete(f"user:{str(user_id)}")

    @staticmethod
    async def __set_cache(user: User):
        from core.cache import cache
        from schema.user import UserModelSchema

        if not await cache.get_user(f"user:{user.tg_id}"):
            user_schema = UserModelSchema(
                id=user.id,
                tg_id=user.tg_id,
                tg_url=user.tg_url,
                first_name=user.first_name,
                last_name=user.last_name,
                tg_username=user.tg_username,
                coins=user.coins,
                is_active=user.is_active,
                is_admin=user.is_admin,
                subscription=user.subscription,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            await cache.set_user(user_schema)

    def check_coin_count(self, user: User):
        if user.coin < 1:
            return

    async def debit_coin(self, user_id: UUID):
        user = await self.repository.get(id=user_id)
        if not user:
            return
        coins_count = user.coin
        self.check_coin_count(user)
        await self.update(user, coin=coins_count - 1)

    async def create(self, **data) -> User:
        if data.get("password"):
            data["password"] = self.get_password_hash(data["password"])
        user = await self.repository.create(**data)
        await self.__set_cache(user)
        return user

    async def update(self, user: User, **data) -> User:
        if data.get("password"):
            data["password"] = self.get_password_hash(data["password"])
        user_upd = await self.repository.update(user, **data)
        await self.__set_cache(user_upd)
        return user_upd

    async def delete(self, user: User) -> None:
        await self.delete_user_cache(user.id)
        await self.repository.delete(user)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        """Сравнивает пароль в БД и из формы, True если соль и пароль верные"""
        return PWD_CONTEXT.verify(
            config.app.secret_key + plain_password, hashed_password
        )

    @staticmethod
    def get_password_hash(password) -> str:
        """Хэширует пароль пользователя, нужно для регистрации или смены пароля"""
        return PWD_CONTEXT.hash(config.app.secret_key + password)


class UserServiceV1:
    def __init__(self):
        self.session = db_conn.session_factory()

    @staticmethod
    async def get_user_subscription(user: User) -> str:
        if user.subscription and user.subscription >= datetime.now():
            return f"Подписка активна до {user.subscription.strftime('%d.%m.%Y')}"
        return "Подписка не активна"

    async def get_user_answers(self, user: User) -> str | None:
        if not user.answers:
            return
        question_ids = [answer.question_id for answer in user.answers]
        async with self.session.begin():
            question_repo = QuestionRepository(session=self.session)
            questions = await question_repo.filter(id={"in": question_ids})

    async def get_user_data(self, user_tg_id: int) -> str | None:
        async with self.session.begin():
            user_repo = UserRepository(session=self.session)
            user = await user_repo.find(tg_id=user_tg_id, select_in_load=[User.answers])
            if not user:
                return

        user_subscription = await self.get_user_subscription(user)
        user_answers = await self.get_user_answers(user)
