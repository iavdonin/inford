"""
Инфраструктура для работы с БД
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DbService:
    """
    Сервисный класс для управления соединением и сессиями. Позволяет
    поддерживать одно соединение на всё приложение и по отдельной сессии на
    каждую транзакцию

    Args:
        url (str): URL подключения к БД
    """

    # pylint: disable=C0301
    # Adopted from https://stackoverflow.com/questions/51124725/sqlalchemy-work-with-connections
    # -to-db-and-sessions-not-clear-behavior-and-pa
    def __init__(self, url):
        self._url = url

        self.engine = create_engine(url, client_encoding='utf8')
        self.session_maker = sessionmaker(bind=self.engine)

    def close(self):
        """
        Закрывает подключение к БД
        """
        self.engine.dispose()
        self.engine = None
        self.session_maker = None

    @contextmanager
    def session_scope(self) -> Session:
        # pylint: disable=E1101
        """
        Контекст-менеджер, предоставляющий сессию с автоматическим коммитом

        Yields:
            (Session): экземпляр сессии

        Raises:
            Exception: любое исключение, возникшее внутри контекста,
                пробрасывается без изменений
        """
        session = self.session_maker(expire_on_commit=False)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
