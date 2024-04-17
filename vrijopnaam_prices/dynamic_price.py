from typing import Iterable

import bs4

from vrijopnaam_prices.time_bounded_price import TimeBoundedPrice


class DynamicPrice:
    def __init__(self, cur: str, unit: str, table: bs4.BeautifulSoup, price_type: str):
        self.__currency = cur.encode().decode('utf-8')
        self.__unit = unit
        self._table = table
        self.__type = price_type

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def unit(self) -> str:
        return self.__unit

    @property
    def type(self) -> str:
        return self.__type

    @property
    def prices(self) -> Iterable[TimeBoundedPrice]:
        raise

    def to_json(self):
        pass
