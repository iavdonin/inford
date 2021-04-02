"""
Модуль класса роутера для поверки вермени и координат.
"""
from typing import List

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from db import DbService
from services import ParseStocks


class StocksDataRouter:
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

    def get_routes(self) -> List[Route]:
        """
        Метод получения списка для starlette.routing.Route

        Returns:
             Список доступных путей REST API
        """
        routes = [
            Route("/parse-stocks", self.parse_stocks, methods=['POST']),
        ]
        return routes

    async def parse_stocks(self, request: Request) -> JSONResponse:
        """
        http метод для забора кадря для поверки времени и координат

        Args:
            request: объект starlette.requests.Request

        Returns:
             сериализованный JSON объект
        """
        return JSONResponse(await self._parse_stocks())

    async def _parse_stocks(self) -> dict:
        amount = await ParseStocks().execute()
        return {"stocks_parsed": amount}
