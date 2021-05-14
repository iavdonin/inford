# pylint: disable=E0401,R0913,W0613
"""
Модуль обработки rest запросов
"""

from starlette.applications import Starlette
from uvicorn import Config, Server

from db import DbService
from .analysis_router import AnalysisRouter


class RESTHandler:
    """ REST handler """

    def __init__(self, db_service: DbService, host: str, port: int, loop):
        """
        Args:
            db_service: сервис для работы с БД
            host: rest api host
            port: rest api port
            loop instance of event loop
        """
        self.host = host
        self.port = port
        self.loop = loop
        self._db_service = db_service

        routes = AnalysisRouter(db_service, self.loop).get_routes()
        self.app = Starlette(debug=True, routes=routes)

    async def run(self):
        """
        Метод для запуска обработчика
        """
        config = Config(host=self.host, port=self.port,
                        http='h11', app=self.app, loop=self.loop)
        server = Server(config)
        await server.serve()
