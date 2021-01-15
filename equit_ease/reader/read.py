from __future__ import annotations
from os import name
from typing import Dict, Any
import requests

from equit_ease.utils.Constants import Constants


class Reader:
    """
    The entrypoint for any submission; This class requests and reads data from two main Yahoo Finance endpoints: `quote` and `chart`.

    There is no parsing, cleaning or structuring done in this class. It's only purpose is to validate the input, send a
    request to an endpoint, verify the responses validity, and return it.

    This implementation aims to follow the Builder design pattern, where the construction of a complex object is separated from 
    its representations. In this specific use case, the data is simply requested for, but there is no parsing or re-structuring.
    That is left to the `Parser` class. This makes it easy for the `Reader` class to be reused, amongst other things.
    """

    def __init__(self, equity: str) -> None:
        # Method Resolution Order: https://stackoverflow.com/questions/42413670/whats-the-difference-between-super-and-parent-class-name
        super().__init__()
        self.equity = equity

    def _get(self, y_finance_formatted_url: str) -> Dict[str, Any]:
        """
        private method which sends the GET request to yahoo finance,
        ensures the response is accurate, and, upon validation, returns it.

        :param y_finance_formatted_url -> ``str``: formatted Yahoo Finance URL (
            see ``build_equity_url`` for what the formatted URL should look like.
        )

        :returns result -> ``Dict[str, Any]``: JSON response object from yahoo finance.
        """
        response = requests.get(y_finance_formatted_url)
        response.raise_for_status()

        result = response.json()

        return result

    @staticmethod
    def _extract_data_from(json_data: Dict[str, Any], key_to_extract: str) -> Any:
        """
        extract ``key_to_extract`` from ``json_data``

        :param json_data -> ``Dict[str, Any]``: JSON response object from any GET /<yahoo_finance_endpoint> which returns JSON data.
        :param key_to_extract -> ``str``: the key to extract from the JSON object.
        :returns result -> ``str`` || ``int``: the value extracted from the key.
        """
        if key_to_extract not in json_data.keys():
            result = "N/A"
        else:
            result = json_data[key_to_extract]
        return result

    @property
    def ticker(self: Reader) -> str:
        """getter for the ticker attribute."""
        return self.__ticker

    @ticker.setter
    def ticker(self: Reader, ticker_value: str) -> None:
        """setter for the ticker attribute."""
        self.__ticker = ticker_value

    @property
    def name(self: Reader) -> str:
        """getter for the name attribute."""
        return self.__name

    @name.setter
    def name(self: Reader, name_value: str) -> None:
        """setter for the name attribute."""
        self.__name = name_value

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
        result = base_chart_url + self.__ticker

        self.chart_url = result
        return True

    def build_equity_quote_url(self: Reader) -> str:
        """
        Creates the quote URL for a given equity.
        This URL is then used for the retrieval of data-points pertaining to
        equity meta-data such as EPS, P/E ratio, 52 wk high and low, etc...

        :param self -> ``Reader``:
        :returns -> ``str``: the formatted URL used to retrieve equity meta-data from yahoo finance.
        """
        base_quote_url = Constants.yahoo_finance_base_quote_url
        # TODO: this could be more robust based off args that can be passed via command-line
        result = base_quote_url + f"?symbols={self.__ticker}"

        self.quote_url = result
        return True

    def build_company_lookup_url(self: Reader) -> str:
        """
        Creates the company lookup URL based on the value passed during instantiation
        of the class.

        :param self -> ``Reader``:
        :return result -> ``str``: the URL to use for self._get()
        """
        base_company_url = Constants.yahoo_finance_co_lookup

        def is_valid(equity: requests.get) -> bool:
            """
            runs a quick validity check to ensure there are quotes matching
            the passed values. If there aren't, a ``ValueError`` is raised.
            """
            """
            Runs a quick validity check for the passed Ticker.

            If error is null, True is returned. Otherwise, False is returned and an error is thrown.

            :param ticker_url -> ``str``: the URL of the ticker.
            """
            json_response = requests.get(equity).json()

            return json_response["quotes"] != []
        
        def build_equity_param() -> str:
            """
            local scope function for building the equity param for the GET request.

            :returns result -> ``str``: the equity param formatted for the GET request.
            """
            split_equity = self.equity.split(" ")
            result = "+".join(split_equity)

            return result
        
        result = base_company_url + build_equity_param()

        if is_valid(result):
            self.company_url = result
            return True
        raise ValueError("Search returned no results.")

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

    def get_equity_company_data(self: Reader, **kwargs) -> Dict[str, Any]:
        """
        the 'equity' value passed upon initialization is used to perform a
        'reverse lookup'.

        The 'equity' value is used to query a Yahoo Finance endpoint which
        returns the long name and ticker symbol (amongst other things) for
        a stock. These two attributes are set with getter/setter methods
        and the ticker symbol is then used throughout the hierarchical
        structure to query yahoo finance.

        :param self -> ``Reader``:
        :returns result -> ``Dict[str, Any]``: Dict containing short name and ticker symbol data.
        """
        json_response = self._get(self.company_url)

        def extract_longname(data):
            """extract 'longname' from JSON object."""
            return self._extract_data_from(data, "longname")

        def extract_ticker(data):
            """extract ticker symbol from JSON object."""
            return self._extract_data_from(data, "symbol")

        def extract_quotes(data):
            """extra all quotes from JSON object."""
            choices = []
            for items in data:
                choices.append(items["shortname"])
            return choices

        long_name = extract_longname(json_response["quotes"][0])
        ticker = extract_ticker(json_response["quotes"][0])

        result = [long_name, ticker]

        if kwargs["force"] == "False":
            result.append(extract_quotes(json_response["quotes"]))
        return result
