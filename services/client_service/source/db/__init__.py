""" Пакет, содержащий инструменты взаимодействия с БД """

from . import model
from .db_service import DbService

__all__ = ['DbService', 'model']
