"""Реализация группы методов Statistics endpoint"""

from datetime import datetime
from zoneinfo import ZoneInfo
from api.stat.service import Service as service

class Statistics:
    """Аналитика и данные"""

    Service = service

    @classmethod
    def ping(cls):
        """ping"""

        url = cls.Service.get_url("/ping")
        #return get_responce(url)


    @classmethod
    def get_detailed_rep(
        cls,
        params: dict = None,
        s_date: datetime = datetime(2024, 1, 29),
        e_date: datetime = datetime.now(ZoneInfo("Europe/Moscow")),
        limit: int = 100000,
        rrd_id: int = 0,
        period: str = "daily",
        datetime_format: str = "%Y-%m-%dT%H:%M:%S"
    ):
        """Отчёт о продажах по реализации"""

        #Период	Лимит	Интервал	Всплеск
        #1 минута	1 запрос	1 минута	1 запрос

        if params is None:

            if period != "daily":
                period = "weekly"

            params = {
                "dateFrom": s_date.strftime(datetime_format),
                "dateTo": e_date.strftime(datetime_format),
                "limit": limit,
                "rrdid": rrd_id,
                "period": period,
            }

        url = cls.Service.get_url("/api/v5/supplier/reportDetailByPeriod")

        #return get_responce(url, params=params), params
