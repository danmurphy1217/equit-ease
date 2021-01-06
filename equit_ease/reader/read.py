from __future__ import annotations
from typing import Dict, Any
import requests

from equit_ease.utils.Constants import Constants


class Reader:
    """
    The entrypoint for any submission; This class requests and reads data from two main Yahoo Finance endpoints: `quote` and `chart`.

    There is no parsing, cleaning or structuring done in this class. It's only purpose is to validate the input, send a
    request to an endpoint, verify the responses validity, and return it.

    This implementation follows the Builder design pattern, where the construction of a complex object is separated from its
    representations. In this specific use case, the data is simply requested for, but there is no parsing or re-structuring.
    That is left to the `Parser` class. This makes it easy for the `Reader` class to be reused, amongst other things.
    """

    def __init__(
        self, equity_to_search: str, date_range: str = None, currency: str = None
    ) -> None:
        # Method Resolution Order: https://stackoverflow.com/questions/42413670/whats-the-difference-between-super-and-parent-class-name
        super().__init__()
        self.equity_to_search = equity_to_search
        self.date_range = date_range
        self.currency = currency

    def _get(self, y_finance_formatted_url: str) -> Dict[str, Any]:
        """
        private method which sends the GET request to yahoo finance,
        ensures the response is accurate, and, upon validation, returns it.

        :param y_finance_formatted_url -> ``str``: formatted Yahoo Finance URL (
            see ``build_equity_url`` for what the formatted URL should look like.
        )

        :returns -> ``Dict[str, Any]``: JSON response object from yahoo finance.
        """
        response = requests.get(y_finance_formatted_url)
        response.raise_for_status()

        return response.json()

    @property
    def build_equity_chart_url(self: Reader) -> str:
        """
        Creates the equity chart URL for a given currency.
        This URL is then used for the retrieval of data-points pertaining to
        the chart.

        :param self -> ``Reader``:
        :returns -> ``str``: the formatted URL used to retrieve the equities chart data from yahoo finance.
        """
        base_chart_url = Constants.yahoo_finance_base_chart_url
        # TODO: this will be more robust based off args that can be passed via command-line
        result = base_chart_url + self.equity_to_search

        def is_valid(ticker_url: str) -> str:
            """
            Runs a quick validity check for the passed Ticker.

            If error is null, True is returned. Otherwise, False is returned and an error is thrown.

            :param ticker_url -> ``str``: the URL of the ticker.
            """
            return requests.get(ticker_url).status_code != 404

        if is_valid(result):
            self.chart_url = result
            return True
        raise ValueError("Invalid Ticker Symbol Passed.")

    @property
    def build_equity_quote_url(self: Reader) -> str:
        """
        Creates the equity quote URL for a given currency.
        This URL is then used for the retrieval of data-points pertaining to
        equity meta-data such as EPS, P/E ratio, 52 wk high and low, etc...

        :param self -> ``Reader``:
        :returns -> ``str``: the formatted URL used to retrieve equity meta-data from yahoo finance.
        """
        base_quote_url = Constants.yahoo_finance_base_quote_url
        # TODO: this will be more robust based off args that can be passed via command-line
        result = base_quote_url + f"?symbols={self.equity_to_search}"

        def is_valid(ticker_url: str) -> str:
            """
            Runs a quick validity check for the passed Ticker.

            If error is null, True is returned. Otherwise, False is returned and an error is thrown.

            :param ticker_url -> ``str``: the URL of the ticker.
            """
            json_response = requests.get(ticker_url).json()

            return json_response['quoteResponse']['result'] != []

        if is_valid(result):
            self.quote_url = result
            return True
        raise ValueError("Invalid Ticker Symbol Passed.")

    def get_equity_chart_data(self: Reader) -> str:
        """
        calls the _get() private method.

        :returns -> ``Dict[str, Any]``: JSON object response from Yahoo Finance
        """
        return self._get(self.chart_url)

    def get_equity_quote_data(self: Reader) -> str:
        """
        calls the _get() private method.

        :returns -> ``Dict[str, Any]``: JSON object response from Yahoo Finance
        """
        return self._get(self.quote_url)
