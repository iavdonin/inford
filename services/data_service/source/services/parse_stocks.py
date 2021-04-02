""" Модуль, содержащий сервисный класс сбора данных об акциях """

from parsing import parse_stocks
from .service_base import ServiceBase


class ParseStocks(ServiceBase):
    """ Сервисный класс, выполняющий сбор данных об акциях и сохранение данных в БД """

    async def execute(self) -> int:
        """
        Выполняет парсинг данных об акциях.

        Returns:
            Количество спарсеных данных.
        """
        amount = parse_stocks()
        return amount
