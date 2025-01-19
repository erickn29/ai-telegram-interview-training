import asyncio

from sqlalchemy import select

from core.database import db_conn
from model import Question, Technology


questions = []


async def add_questions(questions_lst: list[dict]):
    session = db_conn.session_factory()
    async with session.begin():
        for question in questions_lst:
            technology_name = question["technology"].replace(" ", "_").lower()
            result = await session.execute(
                select(Technology).where(Technology.name == technology_name)
            )
            t = result.scalar_one_or_none()
            if not t:
                t = Technology(name=technology_name)
                session.add(t)
                await session.flush()
            q = Question(
                text=question["question"],
                published=True,
                technologies=[
                    t,
                ],
            )
            session.add(q)
    print("done")


if __name__ == "__main__":
    asyncio.run(add_questions(questions))
