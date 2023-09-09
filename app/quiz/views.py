from aiohttp_apispec import querystring_schema, request_schema, response_schema
from aiohttp.web_exceptions import HTTPBadRequest

from app.quiz.models import Answer
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View, Request
from app.web.middlewares import HTTP_ERROR_CODES
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data['title']
        theme = await self.request.app.store.quizzes.get_theme_by_title(title)
        if theme is not None:
            return error_json_response(
                http_status=409,
                status=HTTP_ERROR_CODES[409],
                message='Такая тема уже существует',
                data=self.data
            )
        theme = await self.request.app.store.quizzes.create_theme(title)
        return json_response(data=ThemeSchema().dump(obj=theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        return json_response(
            data={'themes': [ThemeSchema().dump(t) for t in themes]}
        )


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        answers = self.data['answers']
        title = self.data['title']
        theme_id = self.data['theme_id']
        if await self.request.app.store.quizzes.get_theme_by_id(id_=theme_id) is None:
            return error_json_response(
                http_status=404,
                status=HTTP_ERROR_CODES[404],
                data=self.data,
                message='Темы с таким id не существует'
            )
        answers = [Answer(a['title'], a['is_correct']) for a in answers]
        corrects = [answer.is_correct for answer in answers]
        if len(answers) < 2:
            return error_json_response(
                http_status=400,
                status=HTTP_ERROR_CODES[400],
                message='Ответов должно быть больше двух',
                data=self.data,
            )
        if (True not in corrects) ^ (False not in corrects):
            return error_json_response(
                http_status=400,
                status=HTTP_ERROR_CODES[400],
                message=('Должен быть хотя бы один '
                         'правильный и один неправильный ответ'),
                data=self.data,
            )
        question = await self.request.app.store.quizzes.create_question(
            title, theme_id, answers
        )
        return json_response(
            data=QuestionSchema().dump(question)
        )


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = None
        if self.request.query:
            theme_id = self.request.query['theme_id']
        questions = await self.request.app.store.quizzes.list_questions(
            theme_id
        )
        if questions is None:
            return json_response(
                data={}
            )
        return json_response(
            data={'questions': [QuestionSchema().dump(q) for q in questions]}
        )
        
