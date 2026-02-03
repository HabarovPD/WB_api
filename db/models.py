"""Модели таблиц БД"""

import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
)

load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")

SAFE_PASS = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{SAFE_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

Base = declarative_base()
engine = create_engine(DATABASE_URL)

news_type_association = Table(
    "news_type_association",
    Base.metadata,
    Column("news_id", Integer, ForeignKey("ApiNews.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("ApiNewsTypes.id"), primary_key=True),
)


def init_db():
    """создает таблицы базы данных"""

    Base.metadata.create_all(engine)


def drop_all_tables():
    """Удаляет ВСЕ таблицы, привязанные к Base.metadata."""

    Base.metadata.drop_all(engine)


class ApiNewsTypes(Base):
    """Типы новостей API"""

    __tablename__ = "ApiNewsTypes"

    id = Column(Integer, primary_key=True)
    name = Column(Text())

    # Обратное отношение: позволяет получить список новостей для данного типа
    news = relationship(
        "ApiNews", secondary=news_type_association, back_populates="types"
    )


class ApiNews(Base):
    """Новости API"""

    __tablename__ = "ApiNews"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True))
    header = Column(Text())
    content = Column(Text())

    # Отношение многие-ко-многим: позволяет получить список типов для данной новости
    types = relationship(
        "ApiNewsTypes", secondary=news_type_association, back_populates="news"
    )


class Sellers(Base):
    """Данные продавца"""

    __tablename__ = "Sellers"

    sid = Column(String(36), primary_key=True)
    name = Column(Text())
    tradeMark = Column(Text())


class Nomenclature(Base):
    """Номенклатура"""

    __tablename__ = "Nomenclature"

    id = Column(Integer, primary_key=True)
    name = Column(Text())
    isVisible = Column(Boolean, default=True)
    isGroup = Column(Boolean, default=False)
    parentID = Column(Integer, nullable=True)
