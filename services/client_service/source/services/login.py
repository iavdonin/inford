""" Регистрация пользователя """

from typing import Any, Dict, Tuple, Optional

import jwt

from db import DbService
from db.model import ClientProfile

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

    async def execute(self) -> Tuple[str, Optional[str]]:
        async with self._db_service.session_scope as session:
            profile = await session.query(
                ClientProfile
                ).filter(ClientProfile.login == self._params['login']
                ).filter(ClientProfile.password == self._params['password']
                ).one()
            if profile:
                profile_dict = {col.name: getattr(profile, col.name)
                                for col
                                in profile.__table__.columns,
                                if not col.name.startswith('_') and col.name != 'password'}
                token = jwt.encode(profile_dict, self._secret, self._algorithm)
                return token.decode("UTF-8")
