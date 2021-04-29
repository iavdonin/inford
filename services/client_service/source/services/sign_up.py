""" Регистрация пользователя """

from typing import Any, Dict

from db import DbService
from db.model import ClientProfile
from .service_base import ServiceBase


class SignUp(ServiceBase):
    """ Сервисный класс регистрации пользователя """

    def __init__(self, params: Dict[str, Any], db_service: DbService) -> None:
        """
        Args:
            db_service: DbService instance
        """
        super().__init__()
        self._params = params
        self._db_service = db_service

    async def execute(self) -> str:
        try:
            async with self._db_service.session_scope() as session:
                profile = ClientProfile()
                profile.login = self._params['login']
                profile.password = self._params['password']
                profile.email = self._params['email'] if 'email' in self._params.keys() else None
                profile.first_name = self._params['firstname'] if 'firstname' in self._params.keys() \
                    else None
                profile.last_name = self._params['lastname'] if 'lastname' in self._params.keys() \
                    else None
                profile.birth_date = self._params['dateOfBirth'] \
                    if 'dateOfBirth' in self._params.keys() else None
                profile.phone_number = self._params['telephoneNumber'] \
                    if 'telephoneNumber' in self._params.keys() else None
                await session.add(profile)
                return "OK!"
        except:
            return "FAILED!"
