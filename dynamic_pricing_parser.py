import bs4
from dynamic_prices import DynamicPrices, DynamicElectricityPrices, DynamicGasPrices
from typing import Iterable


def parse_prices(htmls: Iterable[str]) -> DynamicPrices:
    prices = DynamicPrices()
    for html in htmls:
        soup = bs4.BeautifulSoup(html, features='html.parser')
        if (result := soup.find('title')) and 'Gas' in result.text:
            table = __parse_gas_prices(soup)
            prices.add(table)
        elif (result := soup.find('title')) and 'Stroom' in result.text:
            table = __parse_electricity_prices(soup)
            prices.add(table)
    return prices


def __parse_electricity_prices(html: bs4.BeautifulSoup):
    pricing_table = html.find('table', class_='pricing-table')
    if not pricing_table:
        raise RuntimeError('Table with class pricing-table was not found')
    return DynamicElectricityPrices(pricing_table)


def __parse_gas_prices(html: bs4.BeautifulSoup):
    pricing_table = html.find('table', class_='pricing-table')
    if not pricing_table:
        raise RuntimeError('Table with class pricing-table was not found')
    return DynamicGasPrices(pricing_table)
