"""
модуль starlette для авторизации через jwt токен.
"""
from typing import Tuple, Union

import jwt
from starlette.authentication import AuthCredentials, AuthenticationError, BaseUser
from starlette_jwt import JWTAuthenticationBackend, JWTUser


class JWTAuthentication(JWTAuthenticationBackend):
    """
    класс проверки аунтификации, используемый как backend аргумент для
     starlette.middleware.authentication.AuthenticationMiddleware
     prefix: ключь токена в header.Authorization
     username_field: ключь в дешифрованном токене с указанием имени пользователя.
     algorithm: Алгоритм проверки JWT
    """

    def __init__(self, secret_key: str, prefix: str,
                 username_field: str = '', algorithm: str = 'HS256'):
        super().__init__(secret_key, algorithm, prefix, username_field)

    async def authenticate(self, request) -> Union[None, Tuple[AuthCredentials, BaseUser]]:
        """
        считывания и проверка данных токена
        """
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        token = self.get_token_from_header(authorization=auth, prefix=self.prefix)
        try:
            payload = jwt.decode(token, key=self.secret_key, algorithms=self.algorithm,
                                 audience=self.audience, options=self.options)
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError(str(exc))
        if self.username_field:
            user = JWTUser(username=payload[self.username_field], token=token,
                           payload=payload)
        else:
            user = JWTUser(username='', token=token,
                           payload=payload)
        return AuthCredentials(["authenticated"]), user
