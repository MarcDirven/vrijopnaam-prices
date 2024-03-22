from vrijopnaam_prices.vrijopnaam_session import VrijOpNaamSession
import vrijopnaam_prices.dynamic_pricing_parser as parser


async def get_prices(username: str, password: str, gas_price: bool = True, electricity_price: bool = True):
    async with VrijOpNaamSession(username, password) as session:
        await session.login()
        htmls = await session.scrape_prices(gas_price, electricity_price)
    return parser.parse_prices(htmls)
