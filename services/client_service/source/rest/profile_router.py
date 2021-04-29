"""
Модуль класса роутера для поверки вермени и координат.
"""
from typing import List

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from starlette.authentication import requires

from db import DbService
from services import SignUp, Login, GetCurrentUser


class ProfileRouter:
    """
    Класс роутера starlette для поверки времени и координат.
    Позволяет оформить все необходимые http методы,
    связанные с заборами данных
    """

    def __init__(self, db_service: DbService, loop):
        """
        Args:
            db_service: сервис для работы с БД
            loop: async loop
        """
        self._db_service = db_service
        self._loop = loop

    def get_routes(self, url_route: str) -> List[Route]:
        """
        Метод получения списка для starlette.routing.Route
        :param url_route: часть http пути
        :return: список роутов
        """
        routes = [
            Route(f"/users/sign-up", self.sign_up, methods=['POST']),
            Route(f"/users/get-current-user", self.get_current_user, methods=['GET']),
            Route(f"/login", self.login, methods=['POST'])
        ]
        return routes

    async def sign_up(self, request: Request):
        params = request.json()
        status = await SignUp(self._db_service).execute(params)
        return Response(status, media_type='text/plain')

    async def login(self, request: Request):
        params = request.json()
        jwt, status = await Login(self._db_service).execute(params)
        return Response(status, media_type='text/plain', headers={'Authorization': f'Bearer {jwt}'})

    @requires('authenticated')
    async def get_current_user(self, request: Request):
        jwt = request.headers['Authorization']
        profile = await GetCurrentUser(self._db_service).execute(jwt)
        return JSONResponse(profile)
