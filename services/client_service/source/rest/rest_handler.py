# pylint: disable=E0401,R0913,W0613
"""
Модуль обработки rest запросов
"""
import asyncio

from db import DbService
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from .cors import (access_control_allow_origin, access_control_allow_methods,
                   access_control_allow_headers)
from .jwt_auth import JWTAuthentication
from .profile_router import ProfileRouter

JWTToken = str


class RESTHandler:
    """ REST handler """

    def __init__(self, db_service: DbService, host: str, port: int, verify_key: str, algorithm: str,
                 loop=None):
        """
        Args:
            db_service: сервис для работы с БД
            host: rest api host
            port: rest api port
            verify_key: jwt secret key
            algorithm: algorithm for signature generation
            loop instance of event loop
        """
        self.host = host
        self.port = port
        self.loop = loop or asyncio.get_event_loop()
        self._verify_key = verify_key
        self._algorithm = algorithm
        self._db_service = db_service

        routes = ProfileRouter(db_service, verify_key, algorithm, self.loop).get_routes()
        self.app = Starlette(debug=True, routes=routes)
        self.app.add_middleware(AuthenticationMiddleware,
                                backend=JWTAuthentication(secret_key=self._verify_key,
                                                          prefix='Bearer',
                                                          algorithm=self._algorithm),
                                )
        self.app.add_middleware(CORSMiddleware,
                                allow_origins=access_control_allow_origin,
                                allow_methods=access_control_allow_methods,
                                allow_headers=access_control_allow_headers)

    async def run(self):
        """
        Метод для запуска обработчика
        """
        config = Config(host=self.host, port=self.port,
                        http='h11', app=self.app, loop=self.loop)
        server = Server(config)
        await server.serve()
