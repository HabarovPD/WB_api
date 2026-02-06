"""Сервисные функции класса Statistics"""

class Service:
    """Сервисные функции класса Statistics"""

    BaseUrl = "https://statistics-api.wildberries.ru"

    @classmethod
    def get_url(cls, endpoint: str) -> str:
        """Возвращает полный адрес endpoint"""

        return f"{cls.BaseUrl}{endpoint}"
