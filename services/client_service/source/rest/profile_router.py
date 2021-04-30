"""
Модуль класса роутера для поверки вермени и координат.
"""
from typing import Dict, List

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from starlette.authentication import requires
from starlette_jwt import JWTUser

from db import DbService
from services import SignUp, Login

JWTToken = str


class ProfileRouter:
    """
    Класс роутера starlette для поверки времени и координат.
    Позволяет оформить все необходимые http методы,
    связанные с заборами данных
    """

    def __init__(self, db_service: DbService, users: Dict[str, str], loop):
        """
        Args:
            db_service: сервис для работы с БД
            users: Маппинг JWT - пользователь
            loop: async loop
        """
        self._db_service = db_service
        self._loop = loop
        self._users = users

    def get_routes(self) -> List[Route]:
        """
        Метод получения списка для starlette.routing.Route.

        Returns:
            Список роутов
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
        params = await request.json()
        jwt, status = await Login(self._db_service).execute(params)
        self._users[jwt] = params['login']
        return Response(status, media_type='text/plain', headers={'Authorization': f'Bearer {jwt}'})

    @requires('authenticated')
    async def get_current_user(self, request: Request):
        return JSONResponse(request.user.payload)
