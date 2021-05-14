# pylint: disable=E0401,R0913,W0613
"""
Модуль обработки rest запросов
"""
import asyncio

from starlette.applications import Starlette
from uvicorn import Config, Server

from .analysis_router import AnalysisRouter


class RESTHandler:
    """ REST handler """

    def __init__(self, host: str, port: int):
        """
        Args:
            host: rest api host
            port: rest api port
            loop instance of event loop
        """
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()

        routes = AnalysisRouter().get_routes()
        self.app = Starlette(debug=True, routes=routes)

    async def run(self):
        """
        Метод для запуска обработчика
        """
        config = Config(host=self.host, port=self.port,
                        http='h11', app=self.app, loop=self.loop)
        server = Server(config)
        await server.serve()
