""" Module that gets the DynamicPrices from a given html """

from typing import Iterable

import bs4

from vrijopnaam_prices._vrijopnaam import VrijOpNaam
from vrijopnaam_prices.dynamic_prices import DynamicElectricityPrices, DynamicGasPrices, DynamicPrices


def parse_prices(htmls: Iterable[str]) -> DynamicPrices:
    dynamic_prices = DynamicPrices()
    for html in htmls:
        table = bs4.BeautifulSoup(html, features='html.parser')
        pricing_table = table.find('table', class_=VrijOpNaam.PRICING_TABLE)

        if not pricing_table:
            raise RuntimeError(f'Table with class "{VrijOpNaam.PRICING_TABLE}" was not found')

        result = table.find('title')
        if result and VrijOpNaam.GAS in result.text:
            prices = DynamicGasPrices(pricing_table)
        elif result and VrijOpNaam.ELECTRICITY in result.text:
            prices = DynamicElectricityPrices(pricing_table)
        else:
            raise RuntimeError('There was no table found with a title')

        if prices:
            dynamic_prices.add(prices)

    return dynamic_prices

