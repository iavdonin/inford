""" Главный исполняемый скрипт сервиса сбора данных """

import asyncio
from argparse import ArgumentParser

from rest import RESTHandler


class AnalysisService:
    """Класс запуска сервиса"""

    def __init__(self, rest_host, rest_port):
        """
        Args:
            rest_port: port of rest handler
            rest_host: host of rest handler
        """
        self.rest_host = rest_host
        self.rest_port = rest_port

    def run(self):
        """Запуск сервиса"""
        rest_handler = RESTHandler(self.rest_host, self.rest_port)
        asyncio.run(rest_handler.run())


def parse():
    """
    Парсинг переменных, передаваемых при запуске
    """
    parser = ArgumentParser()
    parser.add_argument("rest_port", type=int, help="port of rest handler")
    parser.add_argument("rest_host", help="host of rest handler")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    service = AnalysisService(rest_host=args.rest_host, rest_port=args.rest_port)
    service.run()
