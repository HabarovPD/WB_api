"""Основной модуль программы"""

import src.datacollector as DataCollector


if __name__ == "__main__":

    DataCollector.init_db()
    DataCollector.collect_news()
    DataCollector.warehouses()
    #DataCollector.collect_nomenclature()
