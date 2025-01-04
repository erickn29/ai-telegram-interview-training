from model import QuestionTechnology
from repository.base import BaseRepository


class QuestionTechnologyRepository(BaseRepository):
    model = QuestionTechnology

    def __init__(self, session):
        super().__init__(session=session)
