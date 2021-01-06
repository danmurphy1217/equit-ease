from __future__ import annotations
from typing import Dict, Any, List
import json

from equit_ease.reader.read import Reader
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants


class Parser(Reader):
    def __init__(self, equity_to_search, data):
        super().__init__(equity_to_search)
        self.data = data

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

    def _build_dict_repr(
        self, keys_to_extract: List[str], data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        build dictionary representation with the keys to extract and the
        overarching  JSON data structure to extract from.

        :param keys_to_extract -> ``List[str]``: keys to extract.
        :param data -> ``Dict[str, Any``: the data structure to extract from.

        :returns result -> ``Dict[str, Any]``: compiled dictionary containing the keys and their extracted values.
        """
        finalized_data_struct = {}

        for key in list(keys_to_extract):
            finalized_data_struct[key] = self._extract_data_from(data, key)

        return finalized_data_struct


class QuoteParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Quote data."""

    def extract_equity_meta_data(self: QuoteParser) -> Dict[str, Any]:
        """
        extracts meta-data from the GET /quote API call. This meta-data will
        then be used to display a tabular representation of the data in the
        console.

        :params self -> ``Parser``:
        :returns -> ``EquityMeta``: dataclass defined in datatypes/equity_meta.py
        """
        equity_metadata = self.data

        keys_to_extract = Constants.yahoo_finance_quote_keys
        json_data_for_extraction = equity_metadata["quoteResponse"]["result"][0]

        equity_meta_data_struct = self._build_dict_repr(
            keys_to_extract, json_data_for_extraction
        )

        return json.dumps(equity_meta_data_struct)


class ChartParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Chart data."""

    def extract_equity_chart_data(self: ChartParser) -> Dict[str, Any]:
        """
        extracts chart-related data from GET /chart API call. This chart data
        is then used to build a graphical representation of the stock price and/or
        volume (x-axis is time, y-axis is price | volume)
        """
        equity_chart_data = self.data

        json_data_for_extraction = equity_chart_data["chart"]["result"][0][
            "indicators"
        ]["quote"][0]
        keys_to_extract = json_data_for_extraction.keys()

        equity_chart_data_struct = self._build_dict_repr(
            keys_to_extract, json_data_for_extraction
        )

        return json.dumps(equity_chart_data_struct)
