""" Главный исполняемый скрипт сервиса сбора данных """

import asyncio
from argparse import ArgumentParser

from sqlalchemy.engine import create_engine

from db import DbService
from db.model import Base
from rest import RESTHandler


class DataService:
    """Класс запуска сервиса"""

    def __init__(self, db_url, rest_host, rest_port):
        """
        Args:
            db_url: connection string to DB Service instance
            rest_port: port of rest handler
            rest_host: host of rest handler
        """
        self.connection = None
        self.channel = None
        self.rest_host = rest_host
        self.rest_port = rest_port
        self.db_url = db_url
        self.db_service = DbService(db_url)

    def create_tables(self):
        db_url = self.db_url
        if 'asyncpg' in db_url:
            db_url = db_url.replace('+asyncpg', '')
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)

    def run(self):
        """Запуск сервиса"""
        rest_handler = RESTHandler(self.db_service, self.rest_host, self.rest_port)
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
    service = DataService(db_url=args.db_url, rest_host=args.rest_host, rest_port=args.rest_port)
    service.run()
