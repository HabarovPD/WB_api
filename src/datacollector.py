"""Сбор данных и запись в БД"""

from datetime import datetime
from sqlalchemy.orm import sessionmaker
import db.models as Models
from api.wbapi import WbApi


Session = sessionmaker(bind=Models.engine)
session = Session()


def init_db():
    """Инициализирует таблицы БД"""

    Models.init_db()


def collect_news():
    """Обновление новостей"""

    last_news = session.query(Models.ApiNews).order_by(Models.ApiNews.id.desc()).first()
    if last_news:
        data = WbApi.Common.news(None, last_news.id)
    else:
        data = WbApi.Common.news(datetime(2025, 1, 1))

    if data:
        for api_news in data["data"]:
            new_news = Models.ApiNews(
                id=api_news["id"],
                date=datetime.fromisoformat(api_news["date"]),
                header=api_news["header"],
                content=api_news["content"],
            )
            session.merge(new_news)

            for api_news_type in api_news["types"]:
                news_type = Models.ApiNewsTypes(
                    id=api_news_type["id"], name=api_news_type["name"]
                )
                session.merge(news_type)
                new_news.types.append(news_type)

            session.commit()


def collect_user_info():
    """Получение и запись данных пользователя"""

    data = WbApi.Common.seller_info()

    if data:
        seller = Models.Sellers(
            sid=data["sid"], name=data["name"], tradeMark=data["tradeMark"]
        )
        session.merge(seller)
        session.commit()


def collect_nomenclature(locale: str = "ru"):
    """Метод возвращает названия и ID всех родительских категорий для создания карточек товаров"""

    data = WbApi.Content.all_parent(locale)
    if data:
        for parrent in data["data"]:
            nomenclature_group = Models.Nomenclature(
                id=parrent["id"],
                name=parrent["name"],
                isVisible=parrent["isVisible"],
                isGroup=True,
            )
            session.merge(nomenclature_group)

            offset = 0
            limit = 1000
            while True:
                params = {
                    "locale": locale,
                    "parentID": parrent["id"],
                    "limit": limit,
                    "offset": offset,
                }
                inside = WbApi.Content.all_object(params)
                len_inside = len(inside["data"])
                if len_inside:
                    for nom in inside["data"]:
                        nomenclature = Models.Nomenclature(
                            id=nom["subjectID"],
                            name=nom["subjectName"],
                            isVisible=True,
                            isGroup=False,
                            parentID=nom["parentID"],
                        )
                        session.merge(nomenclature)

                    if len_inside < limit:
                        break
                    else:
                        offset = offset + len_inside
                else:
                    break
    session.commit()
