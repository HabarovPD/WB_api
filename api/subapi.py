"""Класс для инъекции методов"""

class BaseSubApi:
    """Клей"""

    base_url = "https://api-seller.wildberries.ru"

    def __init__(self, parent):
        # parent — это экземпляр основного класса WBApi
        self._parent = parent

    def _get_response(self, path, **kwargs):

        url = f"{self.base_url}{path}"
        self._parent.add_limit(url=url)
        return self._parent.get_response(url=url, **kwargs)
