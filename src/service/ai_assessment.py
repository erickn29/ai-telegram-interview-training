from core.config import config
from core.database import db_conn
from model import AIAssessment, Answer, Question, User
from repository.ai_assessment import AIAssessmentRepository
from utils import request


class AIAssessmentServiceV1:
    default_text = "Что-то пошло не так, попробуйте позже"

    def __init__(
        self, question: Question, answer: Answer, user: User, technologies: list[str]
    ):
        self.question = question
        self.answer = answer
        self.user = user
        self.technologies = technologies

    def _get_system_prompt(self) -> str:
        return f"""
        Ты - опытный разработчик. Ты эксперт в таких технологиях как 
        {', '.join(self.technologies)}. 
        На вход тебе подается вопрос и ответ на него. 
        Очень строго и внимательно проверяй правильность и полноту ответа на вопрос. 
        В ответе давай оценку ответу пользователя на вопрос. 
        Если ответ поверхностный и расплывчатый, он не должен оцениваться выше 3.
        Говори что верно и что неверно сказано. Что можно добавить к ответу на вопрос.
        Формат ответа:
        - оценка от 1 до 10 (например 5/10), 1 - очень плохой ответ, 10 - отличный ответ
        - что сказано верно
        - что сказано неверно
        - рекомендации
        """

    def _get_user_answer(self) -> str:
        return f"""
        Вопрос: {self.question.text}.
        Ответ: {self.answer.text}.
        """

    async def _get_model_response(self) -> dict | None:
        response = await request.get_evaluation_request(
            url=config.ai.SERVICE_URL,
            data={
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._get_user_answer()},
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        return response

    async def create_ai_assessment(self, text: str) -> AIAssessment | None:
        session = db_conn.session_factory()
        async with session.begin():
            ai_assessment_repo = AIAssessmentRepository(session=session)
            ai_assessment = await ai_assessment_repo.create(
                text=text,
                user_id=self.user.id,
                question_id=self.question.id,
                answer_id=self.answer.id,
                commit=False,
            )
        return ai_assessment

    @staticmethod
    def _get_score(text: str) -> int:
        if "оценка" in text.lower() and "/10" in text:
            score_string = text.split("/10")[0]
            score_num = score_string.split(" ")[-1]
            if score_num.isdigit():
                return int(score_num)
        return 1

    @staticmethod
    def _normalize_text_to_markdown(text: str) -> str:
        text = (
            text
            # .replace('_', r'\_')
            # .replace('*', r'\*')
            .replace("[", r"\[")
            .replace("]", r"\]")
            .replace("(", r"\(")
            .replace(")", r"\)")
            .replace("~", r"\~")
            # .replace('`', r'\`')
            .replace(">", r"\>")
            .replace("#", r"\#")
            .replace("+", r"\+")
            .replace("-", r"\-")
            .replace("=", r"\=")
            .replace("|", r"\|")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace(".", r"\.")
            .replace("!", r"\!")
        )
        return text

    async def get_ai_assessment(self) -> tuple[AIAssessment, int] | None:
        response = await self._get_model_response()
        if not response:
            return
        try:
            text = response["choices"][0]["message"]["content"].strip()
            text = self._normalize_text_to_markdown(text)
        except (KeyError, IndexError, SyntaxError):
            return
        assessment = await self.create_ai_assessment(text)
        score = self._get_score(text)
        return assessment, score
