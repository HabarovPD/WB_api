"""Класс для инъекции методов"""


class BaseSubApi:
    """Клей"""

    base_url = "https://api-seller.wildberries.ru"

    def __init__(self, wbapi):
        # parent — это экземпляр основного класса WBApi
        self._wbapi = wbapi

    def _get_lim(self, path) -> dict:

        type(path)
        return {"limit": 1, "interval_ms": 60000, "burst": 1}

    def _get_response(self, path, **kwargs):

        url = f"{self.base_url}{path}"
        lim = self._get_lim(path)
        self._wbapi.add_limit(url=url, **lim)
        return self._wbapi.get_response(url=url, **kwargs)
