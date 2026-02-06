"""Реализация группы методов Common endpoint"""

from datetime import datetime
from typing import List
from api.subapi import BaseSubApi
from api.com.user_privilege import UserPrivilege as Privilege


class Common(BaseSubApi):
    """Тарифы, Новости, Информация о продавце"""

    base_url = "https://common-api.wildberries.ru"

    def _get_privilege(
        self, priv_list: List[Privilege], phone: str = None, position: str = None
    ) -> dict:
        """Формирует тело запроса для установки прав доступа"""

        usr_priv = []

        for priv in Privilege:
            is_disabled = priv not in priv_list
            usr_priv.append({"code": priv.value, "disabled": is_disabled})

        json = {
            "access": usr_priv,
            "invite": {"phoneNumber": phone, "position": position},
        }

        return json

    def ping(self) -> dict:
        """Тест соединения с endpoint"""

        return self._get_response("/ping")

    def get_news(self, s_date: datetime = datetime(2000, 1, 1), from_id: int = None) -> dict:
        """Получение новостей"""

        params = {}
        if from_id is not None:
            params["fromID"] = str(from_id)
        else:
            params["from"] = s_date.strftime("%Y-%m-%d")

        return self._get_response("/api/communications/v2/news", params=params)


    # @classmethod
    # def get_seller_info(cls):
    #     """Получение информации о продавце"""

    #     lim = cls.service.get_lim("/api/v1/seller-info")
    #     return get_responce(lim)

    # @classmethod
    # def invite_user(
    #     cls, list_priv: List[UserPrivilege], phone: str = None, position: str = None
    # ):
    #     """Создает приглашение для нового пользователя"""

    #     lim = cls.service.get_lim("/api/v1/invite")
    #     json = cls.service.get_permissions_json(list_priv, phone, position)
    #     return get_responce(lim, method="post", json=json)

    # @classmethod
    # def get_users_list(
    #     cls, invite_only: bool = False, limit: int = 100, offset: int = 0
    # ):
    #     """Метод возвращает список активных или приглашённых пользователей профиля продавца"""

    #     lim = cls.service.get_lim("/api/v1/users")
    #     params = {"IsInviteOnly": invite_only, "limit": limit, "offset": offset}
    #     return get_responce(lim, params=params)

    # @classmethod
    # def change_user_access(cls, ist_priv: List[UserPrivilege]):
    #     """Метод меняет права доступа одному или нескольким пользователям."""

    #     # Некорректен - требует доработки
    #     lim = cls.service.get_lim("/api/v1/users/access")
    #     json = cls.service.get_permissions_json(ist_priv)
    #     return get_responce(lim, method="put", json=json)

    # @classmethod
    # def delete_user(cls, user_id: int):
    #     """Метод удаляет пользователя из списка сотрудников продавца"""

    #     lim = cls.service.get_lim("/api/v1/users/access")
    #     params = {"deletedUserID": user_id}
    #     return get_responce(lim, method="delete", params=params)
