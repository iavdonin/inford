"""
Модуль класса роутера для поверки вермени и координат.
"""
from typing import Dict, List

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from starlette.authentication import requires

from db import DbService
from services import SignUp, Login

JWTToken = str


class ProfileRouter:
    """
    Класс роутера starlette для поверки времени и координат.
    Позволяет оформить все необходимые http методы,
    связанные с заборами данных
    """

    def __init__(self, db_service: DbService, verify_key: str, algorithm: str, loop):
        """
        Args:
            db_service: сервис для работы с БД
            loop: async loop
        """
        self._db_service = db_service
        self._verify_key = verify_key
        self._algorithm = algorithm
        self._loop = loop

    def get_routes(self) -> List[Route]:
        """
        Метод получения списка для starlette.routing.Route.

        Returns:
            Список роутов
        """
        routes = [
            Route(f"/users/sign-up", self.sign_up, methods=['POST']),
            Route(f"/users/get-current-user", self.get_current_user, methods=['GET']),
            Route(f"/login", self.login, methods=['POST']),
            Route(f"/get-analytics", self.get_analytics, methods=['GET']),
            Route(f"/get-recommendations", self.get_recommendations, methods=['GET']),
            Route(f"/add-stock", self.add_stock, methods=['POST'])
        ]
        return routes

    async def sign_up(self, request: Request):
        params = await request.json()
        status = await SignUp(params, self._db_service).execute()
        return Response(status, media_type='text/plain')

    async def login(self, request: Request):
        params = await request.json()
        jwt, status = await Login(params, self._db_service, self._verify_key,
                                  self._algorithm).execute()
        if status == 'OK!':
            return Response(status, media_type='text/plain',
                            headers={'Authorization': f'Bearer {jwt}'})
        else:
            return Response(status, media_type='text/plain')

    @requires('authenticated')
    async def get_current_user(self, request: Request):
        return JSONResponse(request.user.payload)

    @requires('authenticated')
    async def get_analytics(self, request: Request) -> JSONResponse:
        """ Метод для получения аналитики по портфелю """
        portfolio = await request.json()
        return JSONResponse(await self._get_analytics(portfolio))

    @requires('authenticated')
    async def get_recommendations(self, request: Request) -> JSONResponse:
        """ Метод для получения рекомендаций по портфелю """
        portfolio = await request.json()
        return JSONResponse(await self._get_recommendations(portfolio))

    @requires('authenticated')
    async def _get_analytics(self, portfolio) -> dict:
        return GetAnalytics(portfolio).execute()

    @requires('authenticated')
    async def _get_recommendations(self, portfolio) -> dict:
        return GetRecommendations(portfolio).execute()