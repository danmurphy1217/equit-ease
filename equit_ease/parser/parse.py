from typing import Dict, Any

from equit_ease.reader.read import Reader
from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.utils.Constants import Constants

class Parser(Reader):
    def __init__(self, equity_to_search, quote_data, chart_data):
        super().__init__(equity_to_search)
        self.quote_data = quote_data
        self.chart_data = chart_data

    def extract_equity_meta_data(self):
        """
        extracts meta-data from the GET /quote API call. This meta-data will
        then be used to display a tabular representation of the data in the 
        console.

        :params -> ``Parser``:
        :returns -> ``EquityMeta``: dataclass defined in datatypes/equity_meta.py
        """
        equity_metadata = self.quote_data

        keys_to_extract = Constants.yahoo_finance_quote_keys
        equity_meta_mappings = {}

        def extract_data_from(equity_metadata: Dict[str, Any], key_to_extract: str) -> str or int:
            """
            extract ``key_to_extract`` from ``equity_metadata``
            
            :param equity_metadata -> ``Dict[str, Any]``: JSON response object from GET /quote (see Reader.get_equity_quote_data)
            :param key_to_extract -> ``str``: the key to extract from the JSON object.
            :returns result -> ``str`` || ``int``: the value extracted from the key.
            """
            if key_to_extract not in equity_metadata.keys():
                result = "N/A"
            else:
                result = equity_metadata[key_to_extract]
            return result
        
        for key in list(keys_to_extract):
            equity_meta_mappings[key] = extract_data_from(equity_metadata['quoteResponse']['result'][0], key)
        
        return equity_meta_mappings