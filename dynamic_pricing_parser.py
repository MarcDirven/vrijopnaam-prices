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

        prices = None
        if (result := table.find('title')) and 'Gas' in result.text:
            prices = DynamicGasPrices(pricing_table)
        elif (result := table.find('title')) and 'Stroom' in result.text:
            prices = DynamicElectricityPrices(pricing_table)

        if prices:
            dynamic_prices.add(prices)

    return dynamic_prices

