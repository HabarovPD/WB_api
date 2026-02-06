"""Реализация группы методов Common endpoint"""

from datetime import datetime
from api.subapi import BaseSubApi


class Common(BaseSubApi):
    """Тарифы, Новости, Информация о продавце"""

    base_url = "https://common-api.wildberries.ru"

    def _get_lim(self, path) -> dict:

        match path:
            case "/ping":
                lim = {"limit": 1000, "interval_ms": 1, "burst": 1000}
            case "/api/communications/v2/news":
                lim = {"limit": 1, "interval_ms": 60000, "burst": 10}
            case "/api/v1/seller-info":
                lim = {"limit": 1, "interval_ms": 60000, "burst": 10}
            case _:
                lim = {"limit": 1, "interval_ms": 60000, "burst": 1}

        return lim

    def ping(self) -> dict:
        """Тест соединения с endpoint"""

        return self._get_response("/ping")

    def get_news(
        self, s_date: datetime = datetime(2000, 1, 1), from_id: int = None
    ) -> dict:
        """Получение новостей"""

        params = {}
        if from_id is not None:
            params["fromID"] = str(from_id)
        else:
            params["from"] = s_date.strftime("%Y-%m-%d")

        return self._get_response("/api/communications/v2/news", params=params)

    def get_seller_info(self):
        """Получение информации о продавце"""

        return self._get_response("/api/v1/seller-info")
