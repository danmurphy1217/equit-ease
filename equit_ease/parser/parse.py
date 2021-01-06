from typing import Dict, Any
import json
import dataclasses

from equit_ease.reader.read import Reader
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants


class Parser(Reader):
    def __init__(self, equity_to_search, data):
        super().__init__(equity_to_search)
        self.data = data

    @staticmethod
    def extract_data_from(json_data: Dict[str, Any], key_to_extract: str) -> Any:
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

class QuoteParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Quote data."""
    
    def extract_equity_meta_data(self):
        """
        extracts meta-data from the GET /quote API call. This meta-data will
        then be used to display a tabular representation of the data in the
        console.

        :params self -> ``Parser``:
        :returns -> ``EquityMeta``: dataclass defined in datatypes/equity_meta.py
        """
        equity_metadata = self.data

        keys_to_extract_from_yfinance = Constants.yahoo_finance_quote_keys
        json_data_for_extraction = equity_metadata["quoteResponse"]["result"][0]

        equity_meta_mappings = {}

        for key in list(keys_to_extract_from_yfinance):
            equity_meta_mappings[key] = self.extract_data_from(
                json_data_for_extraction, key
            )

        return json.dumps(equity_meta_mappings)

class ChartParser(Parser):
    """contains methods relating to the parsing of Yahoo Finance Chart data."""