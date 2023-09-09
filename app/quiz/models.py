from dataclasses import dataclass

from sqlalchemy import Column, BigInteger, String, ForeignKey, ForeignKeyConstraint, Boolean
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int
    title: str


@dataclass
class Question:
    id: int
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(BigInteger, primary_key=True)
    title = Column(String(50), nullable=False, unique=True)


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    title = Column(String(), nullable=False, unique=True)
    theme_id = Column(ForeignKey('themes.id', ondelete="CASCADE"), nullable=False)
    answers = relationship('AnswerModel', back_populates='question')


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True)
    title = Column(String(), nullable=False)
    is_correct = Column(Boolean(), nullable=False)
    question_id = Column(ForeignKey('questions.id', ondelete='CASCADE'))
    question = relationship('QuestionModel', back_populates='answers')
