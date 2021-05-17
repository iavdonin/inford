"""
Модуль класса роутера для поверки вермени и координат.
"""
from typing import List

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from services import GetAnalytics, GetRecommendations


class AnalysisRouter:
    """
    Класс роутера starlette для получения аналитики и рекомендаций.
    """

    def get_routes(self) -> List[Route]:
        """
        Метод получения списка для starlette.routing.Route

        Returns:
             Список доступных путей REST API
        """
        routes = [
            Route("/get-analytics", self.get_analytics, methods=['GET']),
            Route("/get-recommendations", self.get_recommendations, methods=['GET']),
        ]
        return routes

    async def get_analytics(self, request: Request) -> JSONResponse:
        """ Метод для получения аналитики по портфелю """
        portfolio = await request.json()
        return JSONResponse(await self._get_analytics(portfolio))

    async def get_recommendations(self, request: Request) -> JSONResponse:
        """ Метод для получения рекомендаций по портфелю """
        portfolio = await request.json()
        return JSONResponse(await self._get_recommendations(portfolio))

    async def _get_analytics(self, portfolio) -> dict:
        return await GetAnalytics(portfolio).execute()

    async def _get_recommendations(self, portfolio) -> dict:
        return await GetRecommendations(portfolio).execute()
