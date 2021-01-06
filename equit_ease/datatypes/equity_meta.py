from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass(frozen=True)
class EquityMeta:
    """
    Intermediary data structure utilized for the transportation of Equity Quote metadata
    during the execution of the program. This data is used to display useful infromation
    about a stock (bid, ask, open, close, etc...)
    """

    previous_close: float  # previous days closing stock price
    open: float  # stock price at open
    bid: float  # highest price a buyer will pay
    ask: float  # lowest price a seller will accept
    intra_day_range: Tuple[float, float]  # low - high price for the stock [intra-day]
    fifty_two_wk_range: Tuple[
        float, float
    ]  # low - high price for the stock [last year]
    volume_stats: Dict[
        str, float
    ]  # intra_day volume, monthly avg. volume, and ten_day avg. volume
    market_cap: int  # stock price * shares outstanding
    trailing_and_forward_pe: Dict[str, float]  # trailing and forward PE's
    # trailing PE is current share price / EPS over the previous 12 months ||
    # forward PE is current share price / EPS estimation over next 12 months

    trailing_eps: float  # earnings generated over previous year
    earnings_report_date: int  # unix epoch time
    dividend_rate: float  # annual amount of cash returned to shareholders as a % of a companys share price (market value)
    dividend_yield: float  # amount a company pays shareholders divided by its current stock price
    next_dividend_date: int  # unix epoch time

    # TODO: beta
