from typing import Final, Tuple


class VrijOpNaam:
    VRIJOPNAAM_USERNAME: Final[str] = 'VRIJOPNAAM_USERNAME'
    VRIJOPNAAM_PASSWORD: Final[str] = 'VRIJOPNAAM_PASSWORD'
    USERNAME: Final[str] = 'username'
    PASSWORD: Final[str] = 'password'
    CSRF_TOKEN: Final[str] = 'csrfmiddlewaretoken'
    ASK_STAY_SIGNED_IN: Final[str] = 'ask_stay_signed_in'
    STAY_SIGNED_IN_BTN: Final[str] = 'stay_signed_in_btn'
    URL: Final[str] = 'https://vrijopnaam.app'
    PRICING_ELECTRICITY: Final[str] = 'pricing-electricity'
    PRICING_GAS: Final[str] = 'pricing-gas'
    ON: Final[str] = 'on'
    YES: Final[str] = 'yes'
    SESSION_ID: Final[str] = 'sessionid'
    TODAY: Final[str] = 'Vandaag'
    YESTERDAY: Final[str] = 'Gisteren'
    TOMORROW: Final[str] = 'Morgen'
    PRICING_TABS: Final[Tuple[str, ...]] = (PRICING_GAS, PRICING_ELECTRICITY)
    PRICING_TABLE: Final[str] = 'pricing-table'
