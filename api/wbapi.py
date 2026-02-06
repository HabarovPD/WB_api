"""WbApi"""

import os
from typing import List
import requests
from dotenv import load_dotenv
from api.lim import RateLimit

load_dotenv(override=True)

WB_TOKEN = os.getenv("WB_TOKEN")

class WbApi:
    """WALDBERRIES WEB API CLIENT"""

    def __init__(self):
        """Пустой словарь состояний лимитов"""

        self.limits = {}

    def add_limit(self, url: str, limit: int = 1, interval: int = 1000, burst: int = 1):
        """Инициализирует лимит если он не инициализирован ранее"""

        if url in self.limits:
            return

        self.limits[url] = RateLimit(limit=limit, interval_ms=interval, burst=burst)
        return

    def get_headers(self):
        """генерирует заголовки"""

        return {
            "Authorization": WB_TOKEN,
            "accept": "application/json",
        }

    def get_response(self, url, timeout: int = 20, method: str = 'get', **kwargs):
        """Выполняет запрос и возвращает результат"""

        limiter = self.limits.get(url)
        limiter.wait_and_consume(cost=1)

        if kwargs.get("headers") is None:
            kwargs["headers"] = self.get_headers()

        try:
            response = requests.request(method=method, url=url, timeout=timeout, **kwargs)

            remaining = response.headers.get("X-Ratelimit-Remaining")
            limiter.update_from_headers(remaining=remaining)
            response.raise_for_status()

            if response.status_code == 204:
                return True

            if response.status_code == 429:
                retry_after = response.headers.get("X-Ratelimit-Retry")
                limiter.update_from_headers(remaining=0, retry_after=retry_after)

                return self.get_response(url, timeout, **kwargs)

            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP ошибка: {http_err} {response.text}")
            return None

        except requests.exceptions.RequestException as req_err:
            print(f"Ошибка запроса: {req_err}")
            return None


    # class Content:
    #     """Работа с товарами"""

    #     Name = "Работа с товарами"
    #     BaseUrl = "https://content-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Content.BaseUrl}/ping"
    #         return get_responce(url)

    #     @staticmethod
    #     def all_parent(locale: str = "ru"):
    #         """
    #         Метод возвращает названия и ID всех родительских категорий
    #         для создания карточек товаров например:
    #         Электроника, Бытовая химия, Рукожопие.
    #         """

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/object/parent/all"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def all_object(params: dict):
    #         """
    #         Метод возвращает список названий родительских
    #         категорий предметов и их предметов с ID.
    #         """

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/object/all"
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_object_charcs(subject_id: int, locale: str = "ru"):
    #         """Характеристики предмета"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/object/charcs/{subject_id}"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_colors(locale: str = "ru"):
    #         """Метод возвращает возможные значения характеристики цвет"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/colors"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_kinds(locale: str = "ru"):
    #         """Метод возвращает возможные значения характеристики пол"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/kinds"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_countries(locale: str = "ru"):
    #         """Метод возвращает возможные значения характеристики страна производства"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/countries"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_seasons(locale: str = "ru"):
    #         """Метод возвращает возможные значения характеристики сезон"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/seasons"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_vat(locale: str = "ru"):
    #         """Ставки НДС"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/vat"
    #         params = {"locale": locale}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_tnved(subject_id: int, search: int = None, locale: str = "ru"):
    #         """ТНВЭД"""

    #         url = f"{WbApi.Content.BaseUrl}/content/v2/directory/tnved"
    #         params = {"locale": locale, "subjectID": subject_id, "search": search}
    #         return get_responce(url, params=params)

    #     @staticmethod
    #     def get_brands(subject_id: int, next: int = 0, locale: str = "ru"):
    #         """Бренды предмета"""

    #         url = f"{WbApi.Content.BaseUrl}/api/content/v1/brands"
    #         params = {"locale": locale, "subjectID": subject_id, "next": next}
    #         return get_responce(url, params=params)

    # class ContentSandbox:
    #     """ContentSandbox"""

    #     Name = "Контент (песочница)"
    #     BaseUrl = "https://content-api-sandbox.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.ContentSandbox.BaseUrl}/ping"
    #         return get_responce(url)

    # class Analytics:
    #     """Analytics"""

    #     Name = "Аналитика"
    #     BaseUrl = "https://seller-analytics-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Analytics.BaseUrl}/ping"
    #         return get_responce(url)

    #     class SalesFunel:
    #         """
    #         Статистика карточек товаров за период
    #         Метод формирует отчёт о товарах, сравнивая ключевые показатели — например,
    #         добавления в корзину, заказы и переходы в карточку товара — за текущий период
    #         с аналогичным прошлым. Параметры brandNames,subjectIds, tagIds, nmIds могут
    #         быть пустыми [], тогда в ответе возвращаются все карточки продавца.
    #         Если вы указали несколько параметров, в ответе будут карточки, в которых есть
    #         одновременно все эти параметры. Если карточки не подходят по параметрам запроса,
    #         вернётся пустой ответ [].
    #         Можно получить отчёт максимум за последние 365 дней.
    #         В данных предыдущего периода:
    #         Данные в pastPeriod указаны за такой же период, что и в selectedPeriod
    #         Если дата начала pastPeriod раньше, чем год назад от текущей даты, она будет
    #         приведена к виду: pastPeriod.start = текущая дата — 365 дней
    #         Можно использовать пагинацию.
    #         """

    #         @staticmethod
    #         def get_json() -> dict:
    #             """Возвращает словарь параметров для вызова метода"""

    #             return {
    #                 # Запрашиваемый период
    #                 "selectedPeriod": Service.standart_period(
    #                     end_days_before=0, start_days_delta=182
    #                 ),
    #                 # Период для сравнения
    #                 "pastPeriod": Service.standart_period(
    #                     end_days_before=183, start_days_delta=182
    #                 ),
    #                 # Артикулы WB, по которым нужно составить отчёт.
    #                 # Оставьте пустым, чтобы получить отчёт обо всех товарах,
    #                 # (Array of integers <uint64> [ 0 .. 1000 ] items [ items <uint64 > ])
    #                 "nmIds": [],
    #                 # Список брендов для фильтрации (Array of strings)
    #                 "brandNames": [],
    #                 # Список ID предметов для фильтрации
    #                 # (Array of integers <uint64> [ items <uint64 > ])
    #                 "subjectIds": [],
    #                 # Список ID ярлыков для фильтрации,
    #                 # (Array of integers <uint64> [ items <uint64 > ])
    #                 "tagIds": [],
    #                 # Скрыть удалённые карточки товаров (boolean)
    #                 "skipDeletedNm": False,
    #                 # Параметры сортировки
    #                 "orderBy": {"field": "openCard", "mode": "asc"},
    #                 # Количество карточек товара в ответе (max = 1000)
    #                 "limit": 1000,
    #                 # Сколько элементов пропустить
    #                 "offset": 0,
    #             }

    #         @staticmethod
    #         def get_data(json: dict = get_json()):
    #             """Выполняет запрос"""

    #             url = (
    #                 f"{WbApi.Analytics.BaseUrl}/api/analytics/v3/sales-funnel/products"
    #             )
    #             return get_responce(url, method="post", json=json), json

    #     class SalesFunelWeek:
    #         """
    #         Статистика карточек товаров по дням
    #         Метод возвращает статистику карточек товаров по дням или неделям.
    #         Доступны данные по добавлениям в корзину, заказам,
    #         переходам в карточку товара и так далее.
    #         Можно получить данные максимум за последнюю неделю.
    #         """

    #         @staticmethod
    #         def get_json(
    #             nm_ids: List[int],
    #             period: dict = None,
    #             skip_deleted_items: bool = False,
    #             aggregation_level: Service.WeekDayEnum = Service.WeekDayEnum.Day,
    #         ) -> dict:
    #             """Возвращает словарь параметров для вызова метода"""

    #             if period is None:
    #                 period = Service.standart_period(
    #                     end_days_before=0, start_days_delta=7
    #                 )

    #             return {
    #                 # Запрашиваемый период
    #                 "selectedPeriod": period,
    #                 # Артикулы WB, по которым нужно составить отчёт.
    #                 # (Array of integers <uint64> [ 0 .. 20 ] items [ items <uint64 > ])
    #                 "nmIds": nm_ids,
    #                 # Скрыть удалённые карточки товаров (boolean)
    #                 "skipDeletedNm": skip_deleted_items,
    #                 "aggregationLevel": aggregation_level.value,
    #             }

    #         @staticmethod
    #         def get_data(json: dict):
    #             """Выполняет запрос"""

    #             url = f"{WbApi.Analytics.BaseUrl}/api/analytics/v3/sales-funnel/products/history"
    #             return get_responce(url, method="post", json=json), json

    # class Discounts:
    #     """Discounts"""

    #     Name = "Цены и скидки"
    #     BaseUrl = "https://discounts-prices-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Discounts.BaseUrl}/ping"
    #         return get_responce(url)

    # class DiscountsSandbox:
    #     """DiscountsSandbox"""

    #     Name = "Цены и скидки (песочница)"
    #     BaseUrl = "https://discounts-prices-api-sandbox.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.DiscountsSandbox.BaseUrl}/ping"
    #         return get_responce(url)

    # class Marketplace:
    #     """Marketplace"""

    #     Name = "Маркетплейс"
    #     BaseUrl = "https://marketplace-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Marketplace.BaseUrl}/ping"
    #         return get_responce(url)

    #     @staticmethod
    #     def get_offices():
    #         """Получить список складов WB"""

    #         url = f"{WbApi.Marketplace.BaseUrl}/api/v3/offices"
    #         return get_responce(url)

    #     @staticmethod
    #     def warehouses():
    #         """Метод возвращает список всех складов продавца"""

    #         url = f"{WbApi.Marketplace.BaseUrl}/api/v3/warehouses"
    #         return get_responce(url)

    #     @staticmethod
    #     def get_remaining_goods(warehouse_id: int):
    #         """Получить остатки товаров"""

    #         url = f"{WbApi.Marketplace.BaseUrl}/api/v3/stocks/{warehouse_id}"
    #         return get_responce(url, method="post")

    # class StatisticsSandbox:
    #     """StatisticsSandbox"""

    #     Name = "Статистика (песочница)"
    #     BaseUrl = "https://statistics-api-sandbox.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.StatisticsSandbox.BaseUrl}/ping"
    #         return get_responce(url)

    # class Promotion:
    #     """Promotion"""

    #     Name = "Продвижение"
    #     BaseUrl = "https://advert-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Promotion.BaseUrl}/ping"
    #         return get_responce(url)

    # class PromotionSandbox:
    #     """PromotionSandbox"""

    #     Name = "Продвижение (песочница)"
    #     BaseUrl = "https://advert-api-sandbox.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.PromotionSandbox.BaseUrl}/ping"
    #         return get_responce(url)

    # class Feedbacks:
    #     """Feedbacks"""

    #     Name = "Вопросы и отзывы"
    #     BaseUrl = "https://feedbacks-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Feedbacks.BaseUrl}/ping"
    #         return get_responce(url)

    # class FeedbacksSandbox:
    #     """FeedbacksSandbox"""

    #     Name = "Вопросы и отзывы (песочница)"
    #     BaseUrl = "https://feedbacks-api-sandbox.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.FeedbacksSandbox.BaseUrl}/ping"
    #         return get_responce(url)

    # class Chat:
    #     """Chat"""

    #     Name = "Чат с покупателями"
    #     BaseUrl = "https://buyer-chat-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Chat.BaseUrl}/ping"
    #         return get_responce(url)

    # class Supplies:
    #     """Supplies"""

    #     Name = "Поставки"
    #     BaseUrl = "https://supplies-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Supplies.BaseUrl}/ping"
    #         return get_responce(url)

    # class Returns:
    #     """Returns"""

    #     Name = "Возвраты покупателями"
    #     BaseUrl = "https://returns-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Returns.BaseUrl}/ping"
    #         return get_responce(url)

    # class Documents:
    #     """Documents"""

    #     Name = "Документы"
    #     BaseUrl = "https://documents-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Documents.BaseUrl}/ping"
    #         return get_responce(url)

    # class Finance:
    #     """Finance"""

    #     Name = "Финансы"
    #     BaseUrl = "https://finance-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.Finance.BaseUrl}/ping"
    #         return get_responce(url)

    # class UserManagment:
    #     """UserManagment"""

    #     Name = "Управление пользователями продавца"
    #     BaseUrl = "https://user-management-api.wildberries.ru"

    #     @staticmethod
    #     def ping():
    #         """ping"""

    #         url = f"{WbApi.UserManagment.BaseUrl}/ping"
    #         return get_responce(url)
