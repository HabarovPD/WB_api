"""Сбор данных и запись в БД"""

from datetime import datetime
from sqlalchemy.orm import sessionmaker
import db.models as Models
from api.wbapi import WbApi
import src.service as Service


Session = sessionmaker(bind=Models.engine)
session = Session()


def fill_params(db_table, data_dict):
    """Заполняет параметры таблицы совпадающими параметрами словаря"""

    valid_keys = set(db_table.__mapper__.columns.keys())
    filtered_data = {k: v for k, v in data_dict.items() if k in valid_keys}

    return db_table(**filtered_data)


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


def get_offices():
    """Получает склады WB"""

    data = WbApi.Marketplace.get_offices()
    if data:
        for office in data:
            new_office = Models.Office(**office)
            session.merge(new_office)
        session.commit()


def get_warehouses():
    """Метод возвращает список всех складов продавца"""

    data = WbApi.Marketplace.warehouses()
    if data:
        for warehouses in data:
            new_warehouses = Models.Warehouses(**warehouses)
            session.merge(new_warehouses)
        session.commit()


def get_charcs():
    """Опрос характеристик для всех товаров"""

    nomenclature = session.query(Models.Nomenclature).filter_by(isGroup=False).all()
    for nom in nomenclature:
        data = WbApi.Content.get_object_charcs(nom.id)
        for charc in data["data"]:
            new_charc = fill_params(Models.Characteristics, charc)
            new_charc.id = charc["charcID"]
            session.merge(new_charc)
        session.commit()


def get_others_chr():
    """Прочее"""

    data = WbApi.Content.get_colors()
    if data:
        for d in data["data"]:
            new_rec = Models.Colors(**d)
            session.merge(new_rec)
        session.commit()

    data = WbApi.Content.get_kinds()
    if data:
        for name in data["data"]:
            new_rec = Models.Kinds(name=name)
            session.merge(new_rec)
        session.commit()

    data = WbApi.Content.get_countries()
    if data:
        for d in data["data"]:
            new_rec = Models.Countries(**d)
            session.merge(new_rec)
        session.commit()

    data = WbApi.Content.get_seasons()
    if data:
        for name in data["data"]:
            new_rec = Models.Seasons(name=name)
            session.merge(new_rec)
        session.commit()

    data = WbApi.Content.get_vat()
    if data:
        for name in data["data"]:
            new_rec = Models.Vat(name=name)
            session.merge(new_rec)
        session.commit()


def sales_funel():
    """Статистика карточек товаров за период"""

    data, json = WbApi.Analytics.SalesFunel.get_data()


def sales_funel_week():
    """Статистика карточек по дням"""

    json = WbApi.Analytics.SalesFunelWeek.get_json(
        nm_ids=[781968202, 785196489], aggregation_level=Service.WeekDayEnum.Week
    )
    data, json = WbApi.Analytics.SalesFunelWeek.get_data(json)


def get_detailed_report():
    """Финансовый отчет"""

    params = None
    rep = []

    while True:
        data, params = WbApi.Statistics.DetailedReport.get_rep(params, limit=100)
        if data is None:
            raise "Ошибка при получении запроса"
        if isinstance(data, bool) and data is True:
            break
        rep.extend(data)
        params['rrdid'] = data[len(data)-1]['rrd_id']
    rep = 1
