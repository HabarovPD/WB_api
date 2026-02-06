"""Лимиты запросов"""

import time
import threading


class RateLimit:
    """ "Реализация задержек между запросами"""

    
    def __init__(self, limit: int = 1, interval_ms: int = 60000, burst: int = 1):
        """Инициализация класса"""

        self.limit = limit
        self.max_burst = burst
        self.interval = interval_ms / 1000.0
        self.tokens = float(burst)  # Текущее доступное кол-во
        self.last_update = time.time()
        self.lock = threading.Lock()

    def _replenish(self) -> None:
        """Восполняет токены на основе прошедшего времени."""

        now = time.time()
        passed = now - self.last_update
        new_tokens = passed / self.interval
        self.tokens = min(self.max_burst, self.tokens + new_tokens)
        self.last_update = now

    def wait_and_consume(self, cost: int = 1) -> None:
        """Ожидание"""

        with self.lock:
            while True:
                self._replenish()
                if self.tokens >= cost:
                    self.tokens -= cost
                    return

                # Сколько нужно подождать до появления нужного кол-ва токенов
                wait_time = (cost - self.tokens) * self.interval
                time.sleep(wait_time)

    def update_from_headers(self, remaining, retry_after = None):
        """Синхронизация состояния с реальностью WB."""

        with self.lock:
            if remaining is not None:
                self.tokens = float(remaining)
            if retry_after:
                time.sleep(float(retry_after))
            self.last_update = time.time()
