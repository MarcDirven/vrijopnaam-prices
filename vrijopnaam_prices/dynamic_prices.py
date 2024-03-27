from datetime import datetime
from typing import Any, Iterable

import bs4
from dateutil.relativedelta import relativedelta

import vrijopnaam_prices._parse_utils as pu
from vrijopnaam_prices._vrijopnaam import VrijOpNaam
from vrijopnaam_prices.dynamic_price import DynamicPrice
from vrijopnaam_prices.time_bounded_price import TimeBoundedPrice

__all__ = ["DynamicGasPrices", "DynamicElectricityPrices", "DynamicPrices"]


def _make_prices_json(cur: str, unit: str, prices: Iterable) -> dict[str, Any]:
    return {
        'currency': cur,
        'unit': unit,
        'prices': list(prices)
    }


def _get_date_offset_from_day(day: str) -> datetime:
    time = datetime.now()
    if day == VrijOpNaam.YESTERDAY:
        time -= relativedelta(days=1)
    elif day == VrijOpNaam.TOMORROW:
        time += relativedelta(days=1)
    return time.replace(microsecond=0, hour=0, second=0, minute=0)


class DynamicGasPrices(DynamicPrice):
    def __init__(self, table: bs4.BeautifulSoup):
        cur, unit = pu.get_units(pu.remove_whitespace(table.find_all('th')[1].text))
        super().__init__(cur, unit, table, 'gas')

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        body = self._table.find('tbody')
        all_tr = body.find_all('tr')
        pricing_today = pu.make_float(pu.remove_whitespace(all_tr[0].find_all('td')[2].text))
        pricing_yesterday = pu.make_float(pu.remove_whitespace(all_tr[1].find_all('td')[2].text))

        # Gas day starts at 6 and ends at 6 the next day
        start_today = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
        end_today = start_today + relativedelta(days=1)
        start_yesterday = start_today - relativedelta(days=1)

        yield TimeBoundedPrice(start_today, end_today, pricing_today)
        yield TimeBoundedPrice(start_yesterday, start_today, pricing_yesterday)

    def to_json(self) -> dict[str, Any]:
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

    def get_prices(self) -> Iterable[TimeBoundedPrice]:
        body = self._table.find('tbody').find_all('tr')
        for record in body:
            period, price_left, price_right = record.find_all('td')
            start, end = pu.get_start_end(pu.remove_whitespace(period.find('span').text))
            price_left, price_right = pu.get_price(price_left), pu.get_price(price_right)

            start_hour_left = _get_date_offset_from_day(self.__day_right)
            start_hour_right = _get_date_offset_from_day(self.__day_left)

            end_hour_left = start_hour_left.replace(hour=end)
            end_hour_right = start_hour_right.replace(hour=end)

            # End is 0 (which means start is 23), so this means midnight, next day
            if start == 23 and end == 0:
                end_hour_left += relativedelta(days=1)
                end_hour_right += relativedelta(days=1)

            yield TimeBoundedPrice(start_hour_left.replace(hour=start), end_hour_left, price_left)
            yield TimeBoundedPrice(start_hour_right.replace(hour=start), end_hour_right, price_right)

    def to_json(self) -> dict[str, Any]:
        return _make_prices_json(self.currency, self.unit, (price.to_json() for price in self.get_prices()))


class DynamicPrices:
    def __init__(self):
        self.__dynamic_prices: list[DynamicPrice] = []

    def add(self, d_pricing: DynamicPrice):
        self.__dynamic_prices.append(d_pricing)

    def to_json(self) -> dict[str, dict[str, Any]]:
        return {d.type: d.to_json() for d in self.__dynamic_prices}
