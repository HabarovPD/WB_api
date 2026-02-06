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
    Float,
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


class Characteristics(Base):
    """Характеристики"""

    __tablename__ = "Characteristics"

    id = Column(Integer, primary_key=True)
    name = Column(Text())
    subjectID = Column(Integer)
    subjectName = Column(Text())

    # хараетеристика Обязательна к заполнению
    required = Column(Boolean, default=False)

    # Единица измерения
    unitName = Column(Text())

    # Максимальное количество значений, которое можно присвоить характеристике
    maxCount = Column(Integer)  # "maxCount":0, количество значений не ограничено

    # Характеристика популярна у пользователей (true - да, false - нет)
    popular = Column(Boolean, default=False)

    # Тип данных характеристики, который необходимо использовать
    # \ при создании или редактировании карточек товаров:
    # 1 — массив строк
    # 4 — число (целое либо с десятичной дробью)
    # 0 — характеристика не используется
    charcType = Column(Integer)


class Warehouses(Base):
    """Склады продавца"""

    __tablename__ = "Warehouses"

    # ID склада продавца
    id = Column(Integer, primary_key=True)
    name = Column(Text())

    # ID склада WB
    officeId = Column(Integer)

    # 1 — малогабаритный товар (МГТ)
    # 2 — сверхгабаритный товар (СГТ)
    # 3 — крупногабаритный товар (КГТ+)
    cargoType = Column(Integer)

    # Тип доставки, который принимает склад:
    # 1 — доставка на склад WB (FBS)
    # 2 — доставка силами продавца (DBS)
    # 3 — доставка курьером WB (DBW)
    # 5 — самовывоз (C&C)
    # 6 — экспресс-доставка силами продавца (ЕDBS)
    deliveryType = Column(Integer)

    # Склад удаляется
    # (После удаления склад пропадёт из списка)
    isDeleting = Column(Boolean, default=False)

    # Данные склада обновляются:
    # false — нет
    # true — да, обновление и удаление остатков недоступно
    isProcessing = Column(Boolean, default=False)


class Office(Base):
    """Склады wildberries"""

    __tablename__ = "Office"

    id = Column(Integer, primary_key=True)
    name = Column(Text())
    address = Column(Text())
    city = Column(Text())
    federalDistrict = Column(Text())
    # Широта и долгота
    longitude = Column(Float)
    latitude = Column(Float)

    # Тип товара, который принимает склад:
    # 1 — малогабаритный товар (МГТ)
    # 2 — сверхгабаритный товар (СГТ)
    # 3 — крупногабаритный товар (КГТ+)
    cargoType = Column(Integer)

    # Тип доставки, который принимает склад:
    # 1 — доставка на склад WB (FBS)
    # 2 — доставка силами продавца (DBS)
    # 3 — доставка курьером WB (DBW)
    # 5 — самовывоз (C&C)
    # 6 — экспресс-доставка силами продавца (ЕDBS)
    deliveryType = Column(Integer)

    # Признак того, что склад уже выбран продавцом
    selected = Column(Boolean, default=False)

class Colors(Base):
    """Цвета"""

    __tablename__ = "Colors"
    name = Column(String(255), primary_key=True)
    parentName = Column(String(255))

class Kinds(Base):
    """Пол"""

    __tablename__ = "Kinds"
    name = Column(String(255), primary_key=True)

class Countries(Base):
    """Страны"""

    __tablename__ = "Countries"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    fullName = Column(Text())

class Seasons(Base):
    """Сезоны"""

    __tablename__ = "Seasons"
    name = Column(String(255), primary_key=True)

class Vat(Base):
    """НДС"""

    __tablename__ = "Vat"
    name = Column(String(255), primary_key=True)

class Tnved(Base):
    """ТНВЭД"""

    __tablename__ = "Tnved"
    tnved = Column(String(255), primary_key=True)
    isKiz = Column(Boolean, default=True)

class Brands(Base):
    """Брэнды"""

    __tablename__ = "Brands"
    id = Column(Integer, primary_key=True)
    logoUrl = Column(Text())
    name = Column(Text())
