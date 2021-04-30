""" Главный исполняемый скрипт сервиса сбора данных """

import asyncio
from argparse import ArgumentParser

from db import DbService
from rest import RESTHandler

TMP_SECRET = "89fc4c0db893d94a428f8c64b4c606157c1d65cbd13f34590736b20294fc7de5"


class ClientService:
    """Класс запуска сервиса"""

    def __init__(self, db_url, rest_host, rest_port):
        """
        Args:
            db_url: connection string to DB Service instance
            rest_port: port of rest handler
            rest_host: host of rest handler
        """
        self.rest_host = rest_host
        self.rest_port = rest_port
        self.db_url = db_url
        self.db_service = DbService(db_url)

        self._verify_key = TMP_SECRET
        self.algorithm = 'HS256'

    def run(self):
        """Запуск сервиса"""
        rest_handler = RESTHandler(self.db_service, self.rest_host, self.rest_port,
                                   self._verify_key, self.algorithm)
        asyncio.run(rest_handler.run())


def parse():
    """
    Парсинг переменных, передаваемых при запуске
    """
    parser = ArgumentParser()
    parser.add_argument("db_url", help="DB connection string in SQLAlchemy format")
    parser.add_argument("rest_port", type=int, help="port of rest handler")
    parser.add_argument("rest_host", help="host of rest handler")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    service = ClientService(db_url=args.db_url, rest_host=args.rest_host, rest_port=args.rest_port)
    service.run()
