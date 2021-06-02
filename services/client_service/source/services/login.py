""" Регистрация пользователя """

from typing import Any, Dict, Tuple, Optional, Union

import jwt
from db.model import ClientProfile
from sqlalchemy.future import select

from db import DbService
from .service_base import ServiceBase


class Login(ServiceBase):
    """ Сервисный класс аутентификации пользователя """

    def __init__(self, params: Dict[str, Any], db_service: DbService, secret: str, algorithm: str
                 ) -> None:
        """
        Args:
            db_service: DbService instance
        """
        super().__init__()
        self._params = params
        self._db_service = db_service
        self._secret = secret
        self._algorithm = algorithm

    async def execute(self) -> Tuple[Union[str, None], Optional[str]]:
        async with self._db_service.session_scope() as session:
            profile = await session.execute(
                select(ClientProfile
                ).filter(ClientProfile.login == self._params['login']
                ).filter(ClientProfile.password == self._params['password']
                ))
            profile = profile.first()
            if profile:
                profile_dict = {
                    'login': profile.ClientProfile.login,
                    'email': profile.ClientProfile.email,
                    'firstname': profile.ClientProfile.first_name,
                    'lastname': profile.ClientProfile.last_name,
                    'dateOfBirth': profile.ClientProfile.birth_date,
                    'telephoneNumber': profile.ClientProfile.phone_number
                }
                token = jwt.encode(profile_dict, self._secret, self._algorithm)
                return token, 'OK!'
            else:
                return None, 'FAILED!'
