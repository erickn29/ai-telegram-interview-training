from repository.question import QuestionRepository


async def test_get_unanswered_question_empty_list(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        questions_list = await question_repo.get_questions(
            technologies=["not_exists"],
        )
    assert len(questions_list) == 0


async def test_get_unanswered_question_9_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        questions_list = await question_repo.get_questions(
            technologies=["python", "sql", "django"],
        )
    assert len(questions_list) == 9


async def test_get_unanswered_question_5_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        questions_list = await question_repo.get_questions(
            technologies=["python"],
        )
    assert len(questions_list) == 5
    assert questions["py_question"] in questions_list
    assert questions["py_django_question"] in questions_list
    assert questions["py_sql_question"] in questions_list
    assert questions["sql_py_question"] in questions_list
    assert questions["django_py_question"] in questions_list


async def test_get_unanswered_question_8_questions(
    session, users, technologies, questions
):
    async with session.begin():
        question_repo = QuestionRepository(session=session)
        questions_list = await question_repo.get_questions(
            technologies=["python", "sql"],
        )
    assert len(questions_list) == 8
    assert questions["py_question"] in questions_list
    assert questions["py_django_question"] in questions_list
    assert questions["py_sql_question"] in questions_list
    assert questions["sql_py_question"] in questions_list
    assert questions["django_py_question"] in questions_list
    assert questions["sql_question"] in questions_list
    assert questions["sql_django_question"] in questions_list
    assert questions["django_sql_question"] in questions_list
