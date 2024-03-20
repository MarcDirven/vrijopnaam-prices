import bs4
import parse_utils as pu
from dynamic_prices import DynamicElectricityPrices


def parse_prices(html: str) -> DynamicElectricityPrices:
    html = bs4.BeautifulSoup(html, features='html.parser')
    pricing_table = html.find('table', class_='pricing-table')
    if not pricing_table:
        raise RuntimeError('Table with class pricing-table was not found')
    return __parse_table(pricing_table)


def __parse_table(pricing_table: bs4.BeautifulSoup):
    headers = pricing_table.find('thead').find_all('th')
    today = pu.remove_whitespace(pu.get_header(headers, 'Vandaag').text)

    day = 'Gisteren'
    header_name = pu.get_header(headers, day)
    if not header_name:
        day = 'Morgen'
        header_name = pu.get_header(headers, day)

    currency, power_unit = pu.get_units(today)
    average_today = pu.get_average(today)
    average_tomorrow = pu.get_average(header_name.text)

    return DynamicElectricityPrices(currency, power_unit, average_today, average_tomorrow, pricing_table, day)
