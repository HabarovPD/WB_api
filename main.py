import pandas as pd
from wb_api import WBApi
import time
from dictionary import column_excel
import db.db as db

api = WBApi(api_key="eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwOTA0djEiLCJ0eXAiOiJKV1QifQ.eyJhY2MiOjEsImVudCI6MSwiZXhwIjoxNzg1NjA0NTQyLCJpZCI6IjAxOWMxMjdhLTdhOGEtNzY0Yi1iOTkxLWYxMDVkODY3ZWVjNyIsImlpZCI6MjYwMTM2MTMsIm9pZCI6MTU0MDY1LCJzIjoxMDczNzUwMDUyLCJzaWQiOiIxZDMzYWU0Yi0zOTZlLTQxMDctYWM0NS1jN2Q4YTMyMGE4ZGUiLCJ0IjpmYWxzZSwidWlkIjoyNjAxMzYxM30.ZwcwhoCEMMrpOevzlwMtWRH06FwNp_ioKawAEsGLM6PXtw_zoXdvHXMK-Q0XI6_kHTbQCDVXXCX91LghW0ibxg")

def fetch_financial_report(date_from_str, date_to_str):
    
    stats = api.statistics
    all_reports = []
    rrd_id = 0 # Используем 0 для первого запроса

    print(f"Начинаю загрузку отчета с {date_from_str} по {date_to_str}...")

    while True:
        try:
            # Используем метод get_realization_reports из вашей библиотеки
            reports_batch = stats.get_realization_reports(
                date_from=date_from_str,
                date_to=date_to_str,
                rrdid=rrd_id,
                limit=100000 
            )
            
            if not reports_batch:
                print("Данные закончились или отсутствуют.")
                break

            all_reports.extend(reports_batch)
            print(f"Загружено {len(all_reports)} строк.")

            # Если количество строк меньше лимита, мы достигли конца отчета
            if len(reports_batch) < 100000:
                 break

            # Получаем ID последней записи для следующего запроса
            rrd_id = reports_batch[-1].rrd_id
            time.sleep(10) # Делаем паузу между запросами, чтобы не превышать лимиты WB

        except Exception as e:
            print(f"Произошла ошибка при запросе к API: {e}")
            break

    if all_reports:
        # 1. Преобразуем объекты в DataFrame
        df = pd.DataFrame([vars(r) for r in all_reports]) 
        
        # 2. Удаляем часовые пояса для совместимости с Excel
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]) and df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_localize(None)
        
        # 3. Фильтруем DataFrame, оставляя только те колонки, что есть в словаре (на английском этапе)
        filtered_columns = [col for col in df.columns if col in column_excel.keys()]
        df = df.loc[:, filtered_columns]
        
        # 4. Переименовываем оставшиеся столбцы на русский язык
        df.rename(columns=column_excel, inplace=True)

        # !!! ИСПРАВЛЕННЫЙ БЛОК ДЛЯ УПОРЯДОЧИВАНИЯ !!!
        # Генерируем список русских названий в том порядке, как они идут в словаре
        # и проверяем, что они реально есть в текущем DF (на случай неполного ответа от WB)
        ordered_columns = [
            russian_name 
            for english_key, russian_name in column_excel.items() 
            if russian_name in df.columns
        ]

        # Применяем строгий порядок столбцов
        df = df.loc[:, ordered_columns]
        
        file_name = "wb_report_ordered_russian.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Успех! Сохранено {len(df)} строк в файл {file_name}")
    else:
        print("Данные не получены.")


if __name__ == "__main__":

    db.test_connection()
    
    # Даты должны быть в формате YYYY-MM-DD
    # Обратите внимание: API v5 требует, чтобы date_from был не старше 90 дней
    #fetch_financial_report("2025-10-01", "2026-01-31")