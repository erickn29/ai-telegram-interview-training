import asyncio

from collections.abc import AsyncGenerator, Generator
from typing import Any
from uuid import uuid4

import pytest

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from core.config import config
from model.base import Base
from repository.question import QuestionRepository
from repository.question_technology import QuestionTechnologyRepository
from repository.technology import TechnologyRepository
from repository.user import UserRepository
from repository.user_question import UserQuestionRepository


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def database_url(event_loop):
    async_db_url = config.db.url(db_name=f"test_db_{uuid4().hex[:5]}")
    db_url = async_db_url.replace("postgresql+asyncpg", "postgresql")
    if not database_exists(db_url):
        print(db_url)
        create_database(db_url)

    yield async_db_url

    if database_exists(db_url):
        drop_database(db_url.replace("postgresql+asyncpg", "postgresql"))


@pytest.fixture(scope="session")
async def engine(database_url) -> AsyncGenerator:
    engine = create_async_engine(
        database_url,
        echo=False,
        poolclass=NullPool,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_ = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_() as session:  # type: ignore
        yield session


@pytest.fixture(scope="function")
async def mock_session(session, module_mocker):
    module_mocker.patch("core.database.db_conn.session_factory", return_value=session)
    return session


@pytest.fixture(scope="function")
async def users(session):
    async with session.begin():
        user_repo = UserRepository(session=session)
        user_1 = await user_repo.create(
            tg_id=100,
            tg_url="https://t.me/1",
            first_name="user_1",
            last_name="user_1",
            tg_username="user_1",
            coins=100,
            is_active=True,
            is_admin=False,
            subscription=None,
            password="test_password",
            commit=False,
        )
        user_2 = await user_repo.create(
            tg_id=200,
            tg_url="https://t.me/2",
            first_name="user_2",
            last_name="user_2",
            tg_username="user_2",
            coins=100,
            is_active=True,
            is_admin=False,
            subscription=None,
            password="test_password",
            commit=False,
        )
        user_3 = await user_repo.create(
            tg_id=300,
            tg_url="https://t.me/3",
            first_name="user_3",
            last_name="user_3",
            tg_username="user_3",
            coins=100,
            is_active=True,
            is_admin=False,
            subscription=None,
            password="test_password",
            commit=False,
        )
    return {
        "user_1": user_1,
        "user_2": user_2,
        "user_3": user_3,
    }


@pytest.fixture(scope="function")
async def technologies(session):
    async with session.begin():
        technology_repo = TechnologyRepository(session=session)
        python = await technology_repo.create(name="python", commit=False)
        sql = await technology_repo.create(name="sql", commit=False)
        django = await technology_repo.create(name="django", commit=False)
    return {
        "python": python,
        "sql": sql,
        "django": django,
    }


@pytest.fixture(scope="function")
async def questions(session, technologies, users):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        question_technology_repo = QuestionTechnologyRepository(session=session)
        user_question_repo = UserQuestionRepository(session=session)

        py_question = await question_repo.create(
            text="py_question", complexity=5, published=True, commit=False
        )
        sql_question = await question_repo.create(
            text="sql_question", complexity=5, published=True, commit=False
        )
        django_question = await question_repo.create(
            text="django_question", complexity=5, published=True, commit=False
        )
        py_django_question = await question_repo.create(
            text="py_django_question", complexity=5, published=True, commit=False
        )
        py_sql_question = await question_repo.create(
            text="py_sql_question", complexity=5, published=True, commit=False
        )
        sql_django_question = await question_repo.create(
            text="sql_django_question", complexity=5, published=True, commit=False
        )
        sql_py_question = await question_repo.create(
            text="sql_py_question", complexity=5, published=True, commit=False
        )
        django_py_question = await question_repo.create(
            text="django_py_question", complexity=5, published=True, commit=False
        )
        django_sql_question = await question_repo.create(
            text="django_sql_question", complexity=5, published=True, commit=False
        )
        await question_technology_repo.create(
            question_id=py_question.id,
            technology_id=technologies["python"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=sql_question.id,
            technology_id=technologies["sql"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=django_question.id,
            technology_id=technologies["django"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=py_django_question.id,
            technology_id=technologies["python"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=py_django_question.id,
            technology_id=technologies["django"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=django_py_question.id,
            technology_id=technologies["python"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=django_py_question.id,
            technology_id=technologies["django"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=py_sql_question.id,
            technology_id=technologies["python"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=py_sql_question.id,
            technology_id=technologies["sql"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=sql_py_question.id,
            technology_id=technologies["python"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=sql_py_question.id,
            technology_id=technologies["sql"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=sql_django_question.id,
            technology_id=technologies["django"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=sql_django_question.id,
            technology_id=technologies["sql"].id,
            commit=False,
        )

        await question_technology_repo.create(
            question_id=django_sql_question.id,
            technology_id=technologies["django"].id,
            commit=False,
        )
        await question_technology_repo.create(
            question_id=django_sql_question.id,
            technology_id=technologies["sql"].id,
            commit=False,
        )

        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=py_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=sql_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=django_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=py_django_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=py_sql_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=sql_django_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=sql_py_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=django_py_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_1"].id, question_id=django_sql_question.id, commit=False
        )

        await user_question_repo.create(
            user_id=users["user_2"].id, question_id=py_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_2"].id, question_id=sql_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_2"].id, question_id=py_sql_question.id, commit=False
        )
        await user_question_repo.create(
            user_id=users["user_2"].id, question_id=sql_py_question.id, commit=False
        )
    return {
        "py_question": py_question,
        "sql_question": sql_question,
        "django_question": django_question,
        "py_django_question": py_django_question,
        "py_sql_question": py_sql_question,
        "sql_django_question": sql_django_question,
        "sql_py_question": sql_py_question,
        "django_py_question": django_py_question,
        "django_sql_question": django_sql_question,
    }
