""" Модуль, содержащий сервисный класс сбора данных об акциях """

from parsing import parse_stocks
from .service_base import ServiceBase


class ParseStocks(ServiceBase):
    """ Сервисный класс, выполняющий сбор данных об акциях и сохранение данных в БД """

    def execute(self):
        parse_stocks()
