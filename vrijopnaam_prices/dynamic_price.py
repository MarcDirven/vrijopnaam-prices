from typing import Iterable

from vrijopnaam_prices.time_bounded_price import TimeBoundedPrice


class DynamicPrice:
    def __init__(self, cur: str, unit: str, table: bs4.BeautifulSoup, price_type: str):
        self.__currency = cur
        self.__unit = unit
        self._table = table
        self.__type = price_type

    def __get_currency(self) -> str:
        return self.__currency

    def __get_unit(self) -> str:
        return self.__unit

    def __get_type(self) -> str:
        return self.__type

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        pass

    def to_json(self):
        pass

    type = property(fget=__get_type)
    currency = property(fget=__get_currency)
    unit = property(fget=__get_unit)
