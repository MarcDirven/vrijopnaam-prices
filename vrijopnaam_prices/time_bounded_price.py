from datetime import datetime
from typing import Any


class TimeBoundedPrice:
    def __init__(self, start: datetime, end: datetime, price: float):
        self.__start_time = start
        self.__end_time = end
        self.__price = price

    def _get_price(self) -> float:
        return self.__price

    def _get_start_time(self) -> datetime:
        return self.__start_time

    def _get_end_time(self) -> datetime:
        return self.__end_time

    def to_json(self) -> dict[str, Any]:
        return {
            'startTime': self.hour_start.replace(microsecond=0).isoformat(),
            'endTime': self.hour_end.replace(microsecond=0).isoformat(),
            'price': self.price,
        }

    hour_start = property(fget=_get_start_time)
    hour_end = property(fget=_get_end_time)
    price = property(fget=_get_price)
