from repository.question import QuestionRepository


async def test_get_unanswered_question_empty_list(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        unanswered_questions = await question_repo.get_unanswered_questions(
            user_id=users["user_1"].id,
            technologies=["python", "sql", "django"],
        )
    assert len(unanswered_questions) == 0


async def test_get_unanswered_question_5_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        unanswered_questions = await question_repo.get_unanswered_questions(
            user_id=users["user_2"].id,
            technologies=["python", "sql", "django"],
        )
    assert len(unanswered_questions) == 5
    assert questions["django_question"] in unanswered_questions
    assert questions["py_django_question"] in unanswered_questions
    assert questions["sql_django_question"] in unanswered_questions
    assert questions["django_py_question"] in unanswered_questions
    assert questions["django_sql_question"] in unanswered_questions


async def test_get_unanswered_question_2_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        unanswered_questions = await question_repo.get_unanswered_questions(
            user_id=users["user_2"].id,
            technologies=["python"],
        )
    assert len(unanswered_questions) == 2
    assert questions["django_py_question"] in unanswered_questions
    assert questions["py_django_question"] in unanswered_questions


async def test_get_unanswered_question_4_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        unanswered_questions = await question_repo.get_unanswered_questions(
            user_id=users["user_2"].id,
            technologies=["python", "sql"],
        )
    assert len(unanswered_questions) == 4
    assert questions["django_py_question"] in unanswered_questions
    assert questions["py_django_question"] in unanswered_questions
    assert questions["django_sql_question"] in unanswered_questions
    assert questions["sql_django_question"] in unanswered_questions


async def test_get_unanswered_question_9_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        unanswered_questions = await question_repo.get_unanswered_questions(
            user_id=users["user_3"].id,
            technologies=["python", "sql", "django"],
        )
    assert len(unanswered_questions) == 9
