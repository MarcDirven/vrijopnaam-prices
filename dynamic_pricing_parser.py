import bs4
from dynamic_prices import DynamicPrices, DynamicElectricityPrices, DynamicGasPrices
from typing import Iterable


def parse_prices(htmls: Iterable[str]) -> DynamicPrices:
    dynamic_prices = DynamicPrices()
    for html in htmls:
        table = bs4.BeautifulSoup(html, features='html.parser')
        pricing_table = table.find('table', class_='pricing-table')

        if not pricing_table:
            raise RuntimeError('Table with class pricing-table was not found')

        result = table.find('title')
        if result and 'Gas' in result.text:
            prices = DynamicGasPrices(pricing_table)
        elif result and 'Stroom' in result.text:
            prices = DynamicElectricityPrices(pricing_table)
        else:
            raise RuntimeError('There was no table found with a title')

        if prices:
            dynamic_prices.add(prices)

    return dynamic_prices

