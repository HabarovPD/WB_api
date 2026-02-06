"""Основной модуль программы"""

from api.wbapi import WbApi
from api.com.common import Common
import src.datacollector as DataCollector


if __name__ == "__main__":

    wbapi = WbApi()
    common = Common(parent=wbapi)
    ping = common.ping()
    news = common.get_news()

    print("Done!")
