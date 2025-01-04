from repository.user_question import UserQuestionRepository
from service.question import QuestionServiceV1


async def test_get_question_for_training(
    mock_session, session, users, technologies, questions, mocker
):
    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_2"].id)
        assert len(objects) == 4

    mocker.patch.object(
        QuestionServiceV1, "_get_user_stack", return_value=["python", "sql", "django"]
    )
    question_service = QuestionServiceV1()
    question = await question_service.get_question_for_training(users["user_2"].tg_id)

    assert question is not None
    assert "django" in question.text

    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_2"].id)
        assert len(objects) == 5


async def test_get_question_for_training_repeat(
    mock_session, session, users, technologies, questions, mocker
):
    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_1"].id)
        assert len(objects) == 9

    mocker.patch.object(
        QuestionServiceV1, "_get_user_stack", return_value=["python", "sql", "django"]
    )
    question_service = QuestionServiceV1()
    question = await question_service.get_question_for_training(users["user_1"].tg_id)

    assert question is not None

    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_1"].id)
        assert len(objects) == 9


async def test_get_question_for_training_none(
    mock_session, session, users, technologies, questions, mocker
):
    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_1"].id)
        assert len(objects) == 9

    mocker.patch.object(QuestionServiceV1, "_get_user_stack", return_value=[])
    question_service = QuestionServiceV1()
    question = await question_service.get_question_for_training(users["user_1"].tg_id)

    assert question is not None

    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_1"].id)
        assert len(objects) == 9


async def test_get_question_for_training_new_user(
    mock_session, session, users, technologies, questions, mocker
):
    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_3"].id)
        assert len(objects) == 0

    mocker.patch.object(QuestionServiceV1, "_get_user_stack", return_value=["django"])
    question_service = QuestionServiceV1()
    question = await question_service.get_question_for_training(users["user_3"].tg_id)

    assert question is not None
    assert "django" in question.text

    async with session.begin():
        user_question_repo = UserQuestionRepository(session=session)
        objects = await user_question_repo.filter(user_id=users["user_3"].id)
        assert len(objects) == 1
