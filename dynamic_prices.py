import bs4
from typing import Iterable
import parse_utils as pu
from datetime import datetime, timedelta
from vrijopnaam import VrijOpNaam
from dateutil.relativedelta import relativedelta


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

    def to_json(self) -> dict:
        return {
            'startTime': self.hour_start.replace(microsecond=0).isoformat(),
            'endTime': self.hour_end.replace(microsecond=0).isoformat(),
            'price': self.price,
        }

    hour_start = property(fget=_get_start_time)
    hour_end = property(fget=_get_end_time)
    price = property(fget=_get_price)


def _make_prices_json(cur: str, unit: str, prices: Iterable):
    return {
        'currency': cur,
        'unit': unit,
        'prices': list(prices)
    }


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

    def __get_type(self):
        return self.__type

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        pass

    def _get_date_offset_from_day(self, day: str) -> datetime:
        pass

    def to_json(self):
        pass

    type = property(fget=__get_type)
    currency = property(fget=__get_currency)
    unit = property(fget=__get_unit)


class DynamicGasPrices(DynamicPrice):
    def __init__(self, table: bs4.BeautifulSoup):
        cur, unit = pu.get_units(pu.remove_whitespace(table.find_all('th')[1].text))
        super().__init__(cur, unit, table, 'gas')

    def _get_date_offset_from_day(self, day: str) -> datetime:
        pass

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        body = self._table.find('tbody')
        pricing_now = pu.make_float(pu.remove_whitespace(body.find('tr', class_='pricing-now').find_all('td')[2].text))
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(days=1)
        yield TimeBoundedPrice(start, end, pricing_now)

    def to_json(self) -> dict:
        return _make_prices_json(self.currency, self.unit, (price.to_json() for price in self.get_prices()))


class DynamicElectricityPrices(DynamicPrice):
    def __init__(self, table: bs4.BeautifulSoup):
        _, left, right = table.find('thead').find_all('th')
        left, right = pu.remove_whitespace(left.text), pu.remove_whitespace(right.text)
        currency_l, unit_l = pu.get_units(left)
        currency_r, unit_r = pu.get_units(right)
        assert currency_l == currency_r and unit_l == unit_r

        super().__init__(currency_l, unit_r, table, 'electricity')
        self.__day_left = pu.get_day(left)
        self.__day_right = pu.get_day(right)

    def _get_date_offset_from_day(self, day: str) -> datetime:
        time = datetime.now()
        if day == VrijOpNaam.YESTERDAY:
            time -= relativedelta(days=1)
        elif day == VrijOpNaam.TOMORROW:
            time += relativedelta(days=1)
        return time.replace(microsecond=0, hour=0, second=0, minute=0)

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        body = self._table.find('tbody').find_all('tr')
        for record in body:
            period, price_left, price_right = record.find_all('td')
            start, end = pu.get_start_to(pu.remove_whitespace(period.find('span').text))
            price_left, price_right = pu.get_price(price_left), pu.get_price(price_right)

            start_hour_left = self._get_date_offset_from_day(self.__day_right)
            start_hour_right = self._get_date_offset_from_day(self.__day_left)

            end_hour_left = start_hour_left.replace(hour=end)
            end_hour_right = start_hour_right.replace(hour=end)

            # End is 0 (which means start is 23), so this means midnight, next day
            if end == 0:
                end_hour_left += relativedelta(days=1)
                end_hour_right += relativedelta(days=1)

            yield TimeBoundedPrice(start_hour_left.replace(hour=start), end_hour_left, price_left)
            yield TimeBoundedPrice(start_hour_right.replace(hour=start), end_hour_right, price_right)

    def to_json(self) -> dict:
        return _make_prices_json(self.currency, self.unit, (price.to_json() for price in self.get_prices()))


class DynamicPrices:
    def __init__(self):
        self.__dynamic_prices = []

    def add(self, d_pricing: DynamicPrice):
        self.__dynamic_prices.append(d_pricing)

    def to_json(self) -> dict[list]:
        return {d.type: d.to_json() for d in self.__dynamic_prices}