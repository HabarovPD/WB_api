"""WbApi"""

import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from src.service import SellerAccessCode as Permissions

load_dotenv(override=True)

WB_TOKEN = os.getenv("WB_TOKEN")


def get_headers():
    """генерирует заголовки"""

    result = {
        "Authorization": WB_TOKEN,
        "accept": "application/json",
    }

    return result


def get_responce(
    url,
    method: str = 'get',
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    timeout: int = 20,
):
    """
    Dыполнение запроса
    # Примеры использования:
    # json = {"key": "value"}
    # make_request('https://api.example.com/resource', method='post', json=json)
    # make_request('https://api.example.com/resource/1', method='delete')
    """

    if headers is None:
        headers = get_headers()


    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            timeout=timeout,
            json=json,
            params=params
        )
        response.raise_for_status()  # Вызывает исключение для плохих статусов (4xx или 5xx)

        # Некоторые методы, например DELETE, могут не возвращать JSON-тело (статус 204 No Content)
        if response.status_code == 204:
            return None

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err} {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        # Обработка других ошибок библиотеки requests (например, проблем с сетью)
        print(f"Ошибка запроса: {req_err}")
        return None


def generate_invite_user_json(
    active_codes: set[Permissions], phone_number: str = None, position: str = None
) -> dict:
    """
    Формирует тело запроса API для установки прав доступа.

    :param active_codes: Набор кодов доступа, которые должны быть активированы (disabled=False).
    :param phone_number: Номер телефона для приглашения.
    :param position: Должность для приглашения.
    :return: Полный словарь тела запроса.
    """

    access_list = []

    for code_enum in Permissions:
        is_disabled = code_enum not in active_codes
        access_list.append({"code": code_enum.value, "disabled": is_disabled})

    json = {
        "access": access_list,
        "invite": {"phoneNumber": phone_number, "position": position},
    }

    if phone_number | position:
        invite = {}

        if phone_number:
            invite["phoneNumber"] = phone_number

        if position:
            invite["position"] = position

        json[invite] = invite

    return json


class WbApi:
    """WbApi"""

    class Common:
        """Общее"""

        Name = "Тарифы, Новости, Информация о продавце"
        BaseUrl = "https://common-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Common.BaseUrl}/ping"
            return get_responce(url)

        @staticmethod
        def news(from_date: datetime = datetime(2000, 1, 1), from_id: int = None):
            """Получение новостей"""

            url = f"{WbApi.Common.BaseUrl}/api/communications/v2/news?"

            params = {}
            if from_id is not None:
                params["fromID"] = str(from_id)
            if from_date is not None:
                params["from"] = from_date.strftime("%Y-%m-%d")

            return get_responce(url, params=params)

        @staticmethod
        def seller_info():
            """Получение информации о продавце"""

            url = f"{WbApi.Common.BaseUrl}/api/v1/seller-info"
            return get_responce(url)

        @staticmethod
        def invite_user(permissions, phone: str = None, position: str = None):
            """Создать приглашение для нового пользователя

            url = f"{WbApi.Common.BaseUrl}/api/v1/invite"
            json = generate_invite_user_json(permissions, phone, position)
            method = 'post'
            return get_responce(url, method='post' json=json)
            """
            return permissions, phone, position

        @staticmethod
        def users_list(is_invite_only: bool = False, limit: int = 100, offset: int = 0):
            """Метод возвращает список активных или приглашённых пользователей профиля продавца.

            isInviteOnly=true — список приглашённых пользователей,
            которые ещё не активировали доступ
            isInviteOnly=false или не указан — список активных пользователей
            По каждому пользователю можно получить:
                роль пользователя
                разделы, к которым есть доступы
                статус приглашения
            """

            url = f"{WbApi.Common.BaseUrl}/api/v1/users"
            params = {
                'IsInviteOnly': is_invite_only,
                'limit': limit,
                'offset': offset
            }
            return get_responce(url, params=params)

        @staticmethod
        def change_user_access(permissions):
            """
            Метод меняет права доступа одному или нескольким пользователям.
            Обновляются только права доступа, переданные в параметрах запроса.
            Остальные поля остаются без изменений.
            """

            # Некорректен - требует доработки
            url = f"{WbApi.Common.BaseUrl}/api/v1/users/access"
            json = generate_invite_user_json(permissions)
            return get_responce(url, method='put', json=json)

        @staticmethod
        def delete_user(deleted_user_id: int):
            """
            Метод удаляет пользователя из списка сотрудников продавца.
            Этому пользователю будет закрыт доступ в профиль продавца.
            """
            url = f"{WbApi.Common.BaseUrl}/api/v1/users/access"
            params = {'deletedUserID': deleted_user_id}
            return get_responce(url, method='delete', params=params)

    class Content:
        """Работа с товарами"""

        Name = "Работа с товарами"
        BaseUrl = "https://content-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Content.BaseUrl}/ping"
            return get_responce(url)

        @staticmethod
        def all_parent(locale: str = 'ru'):
            """
            Метод возвращает названия и ID всех родительских категорий
            для создания карточек товаров например:
            Электроника, Бытовая химия, Рукожопие.
            """

            url = f"{WbApi.Content.BaseUrl}/content/v2/object/parent/all"
            params = {"locale": locale}
            return get_responce(url, params=params)

        @staticmethod
        def all_object(params: dict):
            """
            Метод возвращает список названий родительских
            категорий предметов и их предметов с ID.
            """

            url = f"{WbApi.Content.BaseUrl}/content/v2/object/all"
            return get_responce(url, params=params)


    class ContentSandbox:
        """ContentSandbox"""

        Name = "Контент (песочница)"
        BaseUrl = "https://content-api-sandbox.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.ContentSandbox.BaseUrl}/ping"
            return get_responce(url)

    class Analytics:
        """Analytics"""

        Name = "Аналитика"
        BaseUrl = "https://seller-analytics-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Analytics.BaseUrl}/ping"
            return get_responce(url)

    class Discounts:
        """Discounts"""

        Name = "Цены и скидки"
        BaseUrl = "https://discounts-prices-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Discounts.BaseUrl}/ping"
            return get_responce(url)

    class DiscountsSandbox:
        """DiscountsSandbox"""

        Name = "Цены и скидки (песочница)"
        BaseUrl = "https://discounts-prices-api-sandbox.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.DiscountsSandbox.BaseUrl}/ping"
            return get_responce(url)

    class Marketplace:
        """Marketplace"""

        Name = "Маркетплейс"
        BaseUrl = "https://marketplace-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Marketplace.BaseUrl}/ping"
            return get_responce(url)

    class Statistics:
        """Statistics"""

        Name = "Статистика"
        BaseUrl = "https://statistics-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Statistics.BaseUrl}/ping"
            return get_responce(url)

    class StatisticsSandbox:
        """StatisticsSandbox"""

        Name = "Статистика (песочница)"
        BaseUrl = "https://statistics-api-sandbox.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.StatisticsSandbox.BaseUrl}/ping"
            return get_responce(url)

    class Promotion:
        """Promotion"""

        Name = "Продвижение"
        BaseUrl = "https://advert-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Promotion.BaseUrl}/ping"
            return get_responce(url)

    class PromotionSandbox:
        """PromotionSandbox"""

        Name = "Продвижение (песочница)"
        BaseUrl = "https://advert-api-sandbox.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.PromotionSandbox.BaseUrl}/ping"
            return get_responce(url)

    class Feedbacks:
        """Feedbacks"""

        Name = "Вопросы и отзывы"
        BaseUrl = "https://feedbacks-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Feedbacks.BaseUrl}/ping"
            return get_responce(url)

    class FeedbacksSandbox:
        """FeedbacksSandbox"""

        Name = "Вопросы и отзывы (песочница)"
        BaseUrl = "https://feedbacks-api-sandbox.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.FeedbacksSandbox.BaseUrl}/ping"
            return get_responce(url)

    class Chat:
        """Chat"""

        Name = "Чат с покупателями"
        BaseUrl = "https://buyer-chat-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Chat.BaseUrl}/ping"
            return get_responce(url)

    class Supplies:
        """Supplies"""

        Name = "Поставки"
        BaseUrl = "https://supplies-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Supplies.BaseUrl}/ping"
            return get_responce(url)

    class Returns:
        """Returns"""

        Name = "Возвраты покупателями"
        BaseUrl = "https://returns-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Returns.BaseUrl}/ping"
            return get_responce(url)

    class Documents:
        """Documents"""

        Name = "Документы"
        BaseUrl = "https://documents-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Documents.BaseUrl}/ping"
            return get_responce(url)

    class Finance:
        """Finance"""

        Name = "Финансы"
        BaseUrl = "https://finance-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.Finance.BaseUrl}/ping"
            return get_responce(url)

    class UserManagment:
        """UserManagment"""

        Name = "Управление пользователями продавца"
        BaseUrl = "https://user-management-api.wildberries.ru"

        @staticmethod
        def ping():
            """ping"""

            url = f"{WbApi.UserManagment.BaseUrl}/ping"
            return get_responce(url)
