import bs4
from typing import Iterable
import parse_utils as pu
from datetime import datetime, timedelta


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


class DynamicPrice:
    def __init__(self, start: int, end: int, price_today: float, price_tomorrow: float):
        self.__hour_start = start
        self.__hour_end = end
        time = datetime.now()

        self.__price_today = DayPrice(price_today, datetime(time.year, time.month, time.day, start),
                                      datetime(time.year, time.month, time.day, end))
        time += timedelta(days=1)
        self.__price_tomorrow = DayPrice(price_tomorrow, datetime(time.year, time.month, time.day, start),
                                         datetime(time.year, time.month, time.day, end))

    def _get_hour_start(self) -> int:
        return self.__hour_start

    def _get_hour_end(self) -> int:
        return self.__hour_end

    def _get_price_today(self) -> DayPrice:
        return self.__price_today

    def _get_price_tomorrow(self) -> DayPrice:
        return self.__price_tomorrow

    def to_json(self) -> dict:
        return {
            'hourStart': self.hour_start,
            'hourEnd': self.hour_end,
            'today': self.price_today.to_json(),
            'tomorrow': self.__price_tomorrow.to_json()
        }

    hour_start = property(fget=_get_hour_start)
    hour_end = property(fget=_get_hour_end)
    price_today = property(fget=_get_price_today)
    price_tomorrow = property(fget=_get_price_tomorrow)


class DynamicPrices:
    def __init__(self, cur: str, power_unit: str, table: bs4.BeautifulSoup):
        self.__currency = cur
        self.__power_unit = power_unit
        self._table = table

    def __get_currency(self) -> str:
        return self.__currency

    def __get_power_unit(self) -> str:
        return self.__power_unit

    currency = property(fget=__get_currency)
    power_unit = property(fget=__get_power_unit)


class DynamicGasPrices(DynamicPrices):
    def __init__(self, cur: str, power_unit: str, table: bs4.BeautifulSoup):
        super().__init__(cur, power_unit, table)


class DynamicElectricityPrices(DynamicPrices):
    def __init__(self, cur: str, power_unit: str, avg_today: float, avg_tomorrow: float, table: bs4.BeautifulSoup,
                 day: str):
        super().__init__(cur, power_unit, table)
        self.__table_value_left = ''
        self.__table_value_right = ''
        self.__average_today = avg_today
        self.__average_tomorrow = avg_tomorrow
        self.__day = day

    def __get_average_today(self) -> float:
        return self.__average_today

    def __get_average_tomorrow(self) -> float:
        return self.__average_tomorrow

    def __parse_body_today(self) -> Iterable[DynamicPrice]:
        body = self._table.find('tbody').find_all('tr')
        for record in body:
            period, price_today, price_tomorrow = record.find_all('td')
            start, end = pu.get_start_to(pu.remove_whitespace(period.find('span').text))
            price_today = pu.get_price(price_today)
            price_tomorrow = pu.get_price(price_tomorrow)
            yield DynamicPrice(start, end, price_today, price_tomorrow)

    def __get_prices(self):
        return self.__parse_body_today()

    def to_json(self) -> dict:
        return {
            'currency': self.currency,
            'powerUnit': self.power_unit,
            'averageToday': self.average_today,
            'averageTomorrow': self.average_tomorrow,
            'pricesPerHour': [price.to_json() for price in self.prices_per_hour]
        }

    average_today = property(fget=__get_average_today)
    average_tomorrow = property(fget=__get_average_tomorrow)
    prices_per_hour = property(fget=__get_prices)
