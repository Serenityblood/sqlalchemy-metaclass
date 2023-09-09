from aiohttp.web_exceptions import HTTPConflict
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    AnswerModel,
    QuestionModel,
    ThemeModel
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        async with self.app.database.session.begin() as session:
            session.add(theme)
            await session.commit()
        return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_title(self, title: str) -> Theme:
        async with self.app.database.session.begin() as session:
            result = await session.execute(select(ThemeModel).where(ThemeModel.title == title))
            try:
                theme = result.scalar_one()
                return Theme(theme.id, theme.title)
            except NoResultFound:
                return None

    async def get_theme_by_id(self, id_: int) -> Theme:
        async with self.app.database.session.begin() as session:
            result = await session.execute(select(ThemeModel).where(ThemeModel.id == id_))
            try:
                theme = result.scalar_one()
                return Theme(theme.id, theme.title)
            except NoResultFound:
                return None

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session.begin() as session:
            result = await session.execute(select(ThemeModel))
            try:
                themes = result.scalars().all()
                result = [Theme(theme.id, theme.title) for theme in themes]
                return result
            except NoResultFound:
                return None

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        raw_answers: list[AnswerModel] = []
        for answer in answers:
            raw_answers.append(AnswerModel(
                    question_id=question_id,
                    title=answer.title,
                    is_correct=answer.is_correct
                )
            )
        async with self.app.database.session.begin() as session:
            session.add_all(raw_answers)
            await session.commit()
        return [Answer(a.id, a.is_correct) for a in raw_answers]

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = QuestionModel(title=title, theme_id=theme_id)
        async with self.app.database.session.begin() as session:
            session.add(question)
            await session.commit()
        await self.create_answers(question.id, answers)
        return Question(question.id, question.title, question.theme_id, answers)

    async def get_question_by_title(self, title: str) -> Question:
        async with self.app.database.session.begin() as session:
            result = await session.execute(
                select(QuestionModel).options(
                    joinedload(QuestionModel.answers)
                ).where(
                    QuestionModel.title == title
                )
            )
            try:
                question = result.scalars().unique()
                result = []
                for question in question:
                    answers = [Answer(ans.title, ans.is_correct) for ans in question.answers]
                    result.append(Question(question.id, question.title, question.theme_id, answers))
                return Question(question.id, question.title, question.theme_id, answers)
            except NoResultFound:
                return None

    async def list_questions(self, theme_id: int = None) -> list[Question]:
        if theme_id is None:
            async with self.app.database.session.begin() as session:
                try:
                    result = await session.execute(
                        select(QuestionModel).options(
                            joinedload(QuestionModel.answers)
                        )
                    )
                    questions = result.scalars().unique()
                    result = []
                    for question in questions:
                        answers = [Answer(ans.title, ans.is_correct) for ans in question.answers]
                        result.append(Question(question.id, question.title, question.theme_id, answers))
                except NoResultFound:
                    return None
            return result
        async with self.app.database.session.begin() as session:
            try:
                result = await session.execute(select(QuestionModel).options(
                            joinedload(QuestionModel.answers)
                        ).where(QuestionModel.theme_id == theme_id)
                    )
                questions = result.slacars().all()
                result = []
                for question in questions:
                    answers = [Answer(ans.title, ans.is_correct) for ans in question.answers]
                    result.append(Question(question.id, question.title, question.theme_id, answers))
            except NoResultFound:
                return None
            return result
