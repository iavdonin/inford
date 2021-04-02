""" Модуль, содержащий сервисный класс сбора данных об акциях """

import asyncio

from parsing import parse_stocks
from .service_base import ServiceBase


class ParseStocks(ServiceBase):
    """ Сервисный класс, выполняющий сбор данных об акциях и сохранение данных в БД """

    def __init__(self) -> None:
        pass

    async def execute(self) -> int:
        """
        Выполняет парсинг данных об акциях.

        Returns:
            Количество спарсеных данных.
        """
        amount = await parse_stocks()
        return amount
