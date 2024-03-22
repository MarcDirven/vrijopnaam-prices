import bs4
from typing import Tuple


def remove_whitespace(s: str) -> str:
    return ' '.join(s.split())


def get_header(theads: bs4.ResultSet, text: str) -> bs4.PageElement | None:
    return next((t for t in theads if text in t.text), None)


def get_day(d: str) -> str:
    return d.split(' ')[0]


def get_units(s: str) -> Tuple[str, str]:
    currency, unit = s.split(' ')[1].split('/')
    return currency, unit


def make_float(s: str) -> float:
    return float(s.replace(',', '.'))


def get_average(s: str) -> float:
    return make_float(s.split(' ')[-1])


def get_start_end(s: str) -> Tuple[int, int]:
    start, end = s.split(' - ')
    return int(start), int(end)


def get_price(record: bs4.BeautifulSoup) -> float:
    return make_float(remove_whitespace(record.text))


def to_pascal_case(name: str) -> str:
    components = name.split('_')
    return ''.join(components[0].lower() + ''.join(x.title() for x in components[1:]))
