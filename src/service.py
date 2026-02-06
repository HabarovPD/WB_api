"""Сервисные"""

from enum import Enum
from datetime import date, timedelta


def standart_period(
    start: date = date.today(),
    end: date = date.today(),
    end_days_before: int = 0,
    start_days_delta: int = 0,
    date_format: str = "%Y-%m-%d",
) -> dict:
    """Возвращает стандартный период"""

    end_date = end
    if end_days_before:
        end_date -= timedelta(days=end_days_before)

    start_date = min(start, end_date)
    if start_days_delta:
        start_date -= timedelta(days=start_days_delta)

    return {
        "start": start_date.strftime(date_format),
        "end": end_date.strftime(date_format),
    }


class WeekDayEnum(Enum):
    """Агрегаторы запроса - недеоя / день"""

    Week = "week"
    Day = "day"

