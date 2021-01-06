from reader.read import Reader

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
        return
    
    def extract_equity_chart_data(self):
        """
        
        """

# parser.extract_equity_meta_data()
# parser.extract_equity_chart_data()