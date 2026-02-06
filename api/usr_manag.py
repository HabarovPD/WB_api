"""Реализация группы методов User managment endpoint"""

from typing import List
from api.subapi import BaseSubApi
from api.enums.user_privilege import UserPrivilege as Privilege


class UserManager(BaseSubApi):
    """Управление пользователями"""

    base_url = "https://user-management-api.wildberries.ru"

    def _get_lim(self, path) -> dict:

        match path:
            case "/api/v1/invite":
                lim = {"limit": 1, "interval_ms": 1000, "burst": 5}
            case "/api/v1/users":
                lim = {"limit": 1, "interval_ms": 1000, "burst": 5}
            case "/api/v1/users/access":
                lim = {"limit": 1, "interval_ms": 1000, "burst": 5}
            case "/api/v1/user":
                lim = {"limit": 1, "interval_ms": 1000, "burst": 10}
            case _:
                lim = {"limit": 1, "interval_ms": 60000, "burst": 1}

        return lim

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

    def invite_user(
        self, list_priv: List[Privilege], phone: str = None, position: str = None
    ):
        """Создает приглашение для нового пользователя"""

        json = self._get_privilege(list_priv, phone, position)
        return self._get_response("/api/v1/invite", method="post", json=json)

    def get_users_list(
        self, invite_only: bool = False, limit: int = 100, offset: int = 0
    ):
        """Метод возвращает список активных или приглашённых пользователей профиля продавца"""

        params = {"IsInviteOnly": invite_only, "limit": limit, "offset": offset}
        return self._get_response("/api/v1/users", params=params)

    def change_user_access(self, ist_priv: List[Privilege]):
        """Метод меняет права доступа одному или нескольким пользователям."""

        # Некорректен - требует доработки
        json = self._get_privilege(ist_priv)
        return self._get_response("/api/v1/users/access", method="put", json=json)

    def delete_user(self, user_id: int):
        """Метод удаляет пользователя из списка сотрудников продавца"""

        params = {"deletedUserID": user_id}
        return self._get_response("/api/v1/user", method="delete", params=params)
