"""Перечисление - права пользователей"""

from enum import Enum


class UserPrivilege(Enum):
    """Перечисление - права пользователей"""

    BALANCE = "balance"
    # brands - Управление брендами
    BRANDS = "brands"
    # changeJam - Доступ к подключению подписки Джем:
    # А/Б тесты, отметки на фото, автозапуски видео, сравнение карточек
    CHANGE_JAM = "changeJam"
    # discountPrice - Изменение цен на товары, управление скидками и акциями
    DISCOUNT_PRICE = "discountPrice"
    # finance - Финансовая аналитика. Статистика по балансу, финансовые отчёты, история платежей
    FINANCE = "finance"
    # showcase - Управление витриной магазина
    SHOWCASE = "showcase"
    # suppliersDocuments - Просмотр и скачивание документов по работе с площадкой
    SUPPLIERS_DOCUMENTS = "suppliersDocuments"
    # supply - Создание и управление поставками FBW
    SUPPLY = "supply"
    # feedbacksQuestions - Просмотр и ответы на вопросы и отзывы покупателей, жалобы на отзывы
    FEEDBACKS_QUESTIONS = "feedbacksQuestions"
    # questions - Просмотр и ответы на вопросы покупателей
    QUESTIONS = "questions"
    # pinFeedbacks - Возможность закреплять и откреплять отзывы
    PIN_FEEDBACKS = "pinFeedbacks"
    # pointsForReviews - Баллы за отзывы
    POINTS_FOR_REVIEWS = "pointsForReviews"
    # feedbacks - Просмотр и ответы на отзывы покупателей
    FEEDBACKS = "feedbacks"
    # wbPoint - WB Point
    WB_POINT = "wbPoint"
