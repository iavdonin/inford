""" Модель данных сервиса """

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClientProfile(Base):
    __tablename__ = "client_profile"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    login = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    birth_date = Column(Date)
