from datetime import datetime
import _parse_utils as pu


class DayPrice:
    def __init__(self, price: float, start_time: datetime, end_time: datetime):
        self.__price = price
        self.__start_time = start_time
        self.__end_time = end_time

    def to_json(self) -> dict:
        converted_dict = {}
        for name in vars(self):
            converted = pu.to_pascal_case(name.removeprefix('_DayPrice__'))
            value = getattr(self, name)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            converted_dict[converted] = value
        return converted_dict

    def _get_price(self) -> float:
        return self.__price

    def _get_start_time(self) -> datetime:
        return self.__start_time

    def _get_end_time(self) -> datetime:
        return self.__end_time

    price = property(fget=_get_price)
    start_time = property(fget=_get_start_time)
    end_time = property(fget=_get_end_time)
