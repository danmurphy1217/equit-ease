import json
import os

from equit_ease.parser.parse import ChartParser
import unittest

def read_quote_fixture(fpath: str):
    fixture_file_path = os.path.join(os.path.dirname(__file__), fpath)
    with open(fixture_file_path, "r") as quote_fixture:
        data = json.loads(quote_fixture.read())
    return data

class TestChartParserMethods(unittest.TestCase):
    """testing methods from the ChartParser class."""

    def setUp(self):
        self.equity = "Apple"
        self.data_fixture = read_quote_fixture("fixtures/chart.json")
        self.errant_data_fixture = read_quote_fixture("fixtures/chart-errant.json")
        self.parser = ChartParser(self.equity, self.data_fixture)

    def tearDown(self):
        self.ticker_to_search = None
        self.data_fixture = None
        self.parser = ChartParser
    
    def test_extract_equity_chart_data_keys(self):
        """
        test extract_equity_chart_data() #1 -> pass.

        check that the response from extract_equity_chart_data() is a
        tuple containing the following keys. Additionally, for each key,
        check that non-standardized values are not equal to `chart_data`
        and standardized values are equal to `chart_data`.
        )
        """
        keys = (
            "low",
            "high",
            "open",
            "close",
            "volume"
        )
        chart_data = self.parser.extract_equity_chart_data()

        for i, key in enumerate(keys):
            filtered_chart_data = self.data_fixture["chart"]["result"][0]["indicators"]["quote"][0][key]
        
            # data is not standardized, so None values appear
            self.assertNotEqual(filtered_chart_data, chart_data[i])
            # data is standardized
            self.assertEqual(self.parser.standardize(filtered_chart_data), chart_data[i])
