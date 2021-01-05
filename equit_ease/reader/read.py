import requests
from equit_ease.utils.Constants import Constants


class Reader:
    def __init__(
        self, equity_to_search: str, date_range: str = None, currency: str = None
    ) -> None:
        # Method Resolution Order: https://stackoverflow.com/questions/42413670/whats-the-difference-between-super-and-parent-class-name
        super().__init__()
        self.equity_to_search = equity_to_search
        self.date_range = date_range
        self.currency = currency

    def build_equity_url_for(self) -> str:
        """
        Creates the equity backend URL (yahoo finance) for a given currency.
        This URL is then used for the retrieval of data-points pertaining to
        the equity.

        :param self -> ``Reader``:
        :returns -> ``str``: the formatted URL used to retrieve the equities data from yahoo finance.
        """
        base_url = Constants.yahoo_finance_base_chart_url
        result = base_url + self.equity_to_search

        def is_valid(ticker_url: str) -> str:
            """
            Runs a quick validity check for the passed Ticker. 

            If error is null, True is returned. Otherwise, False is returned and an error is thrown.

            :param ticker_url -> ``str``: the URL of the ticker.
            """
            return requests.get(ticker_url).status_code != 404

        if is_valid(result):
            return result
        raise ValueError("Invalid Ticker Symbol Passed.")
