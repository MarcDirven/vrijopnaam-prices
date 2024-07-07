from datetime import datetime
from typing import Any


class TimeBoundedPrice:
    def __init__(self, start: datetime, end: datetime, price: float, day_name: str):
        self.__start_time = start
        self.__end_time = end
        self.__price = price
        self.__day_name = day_name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def hour_start(self) -> datetime:
        return self.__start_time

    @property
    def hour_end(self) -> datetime:
        return self.__end_time

    @property
    def day_name(self) -> str:
        return self.__day_name

    def to_json(self) -> dict[str, Any]:
        return {
            'startTime': self.hour_start.replace(microsecond=0).isoformat(),
            'endTime': self.hour_end.replace(microsecond=0).isoformat(),
            'price': self.price,
            'dayName': self.day_name
        }
