from datetime import datetime
from typing import Any


class TimeBoundedPrice:
    def __init__(self, start: datetime, end: datetime, price: float, day_name: str):
        self.__start_time = start
        self.__end_time = end
        self.__price = price
        self.__day_name = day_name

    def _get_price(self) -> float:
        return self.__price

    def _get_start_time(self) -> datetime:
        return self.__start_time

    def _get_end_time(self) -> datetime:
        return self.__end_time

    def _get_day_name(self) -> str:
        return self.__day_name

    def to_json(self) -> dict[str, Any]:
        return {
            'startTime': self.hour_start.replace(microsecond=0).isoformat(),
            'endTime': self.hour_end.replace(microsecond=0).isoformat(),
            'price': self.price,
            'dayName': self.day_name
        }

    hour_start = property(fget=_get_start_time)
    hour_end = property(fget=_get_end_time)
    price = property(fget=_get_price)
    day_name = property(fget=_get_day_name)
