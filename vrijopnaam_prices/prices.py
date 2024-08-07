import sys

import vrijopnaam_prices._dynamic_pricing_parser as parser
from vrijopnaam_prices._vrijopnaam import VrijOpNaam
from vrijopnaam_prices._vrijopnaam_session import ConditionalFetch, VrijOpNaamSession

if sys.version_info[0] < 3 and sys.version_info[1] < 10:
    raise RuntimeError("You're not running Python 3.10 or higher, be using Python 3.10 at least")


async def get_prices(username: str, password: str, gas_price: bool = True, electricity_price: bool = True):
    to_fetch = (ConditionalFetch(gas_price, VrijOpNaam.PRICING_GAS),
                ConditionalFetch(electricity_price, VrijOpNaam.PRICING_ELECTRICITY))

    async with VrijOpNaamSession(username, password) as session:
        await session.login()
        htmls = await session.scrape_prices(to_fetch)
        return await parser.parse_prices(htmls)
