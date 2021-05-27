"""
Модуль класса роутера для поверки вермени и координат.
"""
import json
from collections import defaultdict
from typing import List

import aiohttp
from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route

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
        self._tmp_portfolio_storage = defaultdict(dict)
        self._tmp_money_available_storage = dict()

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
            Route(f"/get-recommendations", self.save_money_available, methods=['POST']),
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
        current_user = request.user.payload
        current_user['stocks'] = self._tmp_portfolio_storage[current_user['login']]
        return JSONResponse(current_user)

    @requires('authenticated')
    async def get_analytics(self, request: Request) -> JSONResponse:
        """ Метод для получения аналитики по портфелю """
        login = request.user.payload['login']
        portfolio = self._tmp_portfolio_storage[login]
        request_payload = json.dumps(portfolio)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://analysis_service:5000/get-analytics',
                                   data=request_payload) as response:
                return JSONResponse(await response.json())

    @requires('authenticated')
    async def get_recommendations(self, request: Request) -> JSONResponse:
        """ Метод для получения рекомендаций по портфелю """
        login = request.user.payload['login']
        try:
            money_available = self._tmp_money_available_storage.pop(login)
        except KeyError:
            return Response('Money available is not specified!', media_type='text/plain')
        portfolio = self._tmp_portfolio_storage[login]
        analysis_data = {
            'portfolio': portfolio,
            'money_available': money_available
        }
        request_payload = json.dumps(analysis_data)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://analysis_service:5000/get-recommendations',
                                   data=request_payload) as response:
                return JSONResponse(await response.json())

    @requires('authenticated')
    async def save_money_available(self, request: Request) -> Response:
        """ Костыль для хранения количества доступных денег при формировании рекомендаций """
        request_payload = await request.json()
        login = request.user.payload['login']
        self._tmp_money_available_storage[login] = float(request_payload['money_available'])
        return Response('OK!', media_type='text/plain')

    @requires('authenticated')
    async def add_stock(self, request: Request) -> Response:
        login = request.user.payload['login']
        new_stock = await request.json()
        name = new_stock['stock']
        amount = new_stock['col']
        self._tmp_portfolio_storage[login].update({name: amount})
        return Response('OK!', media_type='text/plain')
