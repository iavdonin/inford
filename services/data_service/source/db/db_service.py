"""
модель сервисного класса для управления соединением и сессиями.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, sessionmaker


class AsyncSessionContext:
    """
    Базовый класс контекст-менеджера, предоставляющий сессию с
    автоматическим коммитом
    """

    def __init__(self, session: AsyncSession):
        """
        :param session: Экземпляр сессии sqlalchemy
        """
        self.session = session

    async def __aenter__(self):
        """
        Асинхронный метод вызова контекстного менеджера
        :return: экземпляр AsyncSession
        """
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Асинхронный метод выхода из контекстного менеджера
        """
        try:
            if exc_type is not None:
                raise exc_val
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
        finally:
            await self.session.close()


class DbService:
    """
    Сервисный класс для управления соединением и сессиями. Позволяет
    поддерживать одно соединение на всё приложение и по отдельной сессии на
    каждую транзакцию
    В случае исключение в stderr будет выкинуто сообщение и
    выкинется исключение errors.DBServiceError

    Args:
        url (str): URL подключения к БД

    Example:
        db_session = DbService("postgresql://postgres:postgres@localhost/db")
        with db_session.session_scope() as session:
            session.query(Model).all()
            data = Model(field1=1, field2="2")
            session.add(data)
    Async Example:
        db_session = DbService("postgresql+asyncpg:://postgres:postgres@localhost/db")
        with db_session.async_session_scope() as session:
            await session.query(Model).all()
            data = Model(field1=1, field2="2")
            await session.add(data)
    """

    # pylint: disable=C0301
    # Adopted from https://stackoverflow.com/questions/51124725/sqlalchemy-work-with-connections
    # -to-db-and-sessions-not-clear-behavior-and-pa
    def __init__(self, url: str):
        """
        url - connection url
        """
        self._url = url
        self.engine = create_engine(url, client_encoding='utf8')
        self.session_maker = sessionmaker(bind=self.engine, class_=Session)
        self.async_session_maker = sessionmaker(bind=self.engine, class_=AsyncSession)

    def close(self):
        """
        Закрывает подключение к БД
        """
        self.engine.dispose()
        self.engine = None
        self.session_maker = None

    def session_scope(self) -> AsyncSessionContext:
        # pylint: disable=E1101
        """
        Возвращает объект AsyncSessionContext с хранимой сессией
        """
        if self._url.find("asyncpg") == -1:
            raise ValueError("can't find async driver in connection string")
        session_ = self.async_session_maker(expire_on_commit=False, class_=AsyncSession)
        return AsyncSessionContext(session_)
