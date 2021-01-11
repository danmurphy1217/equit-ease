import unittest

from equit_ease.parser.parse import QuoteParser

class TestQuoteParserMethods(unittest.TestCase):
    def setUp(self):
        self.equity = "Apple"
        self.data_fixture = {"one": "first key", "two": None}
        self.parser = QuoteParser(self.equity, self.data_fixture)

    def tearDown(self):
        self.ticker_to_search = None
        self.data_fixture = None
        self.parser = QuoteParser
    
    def test_extract_equity_meta_data(self):
        """
        test extract_equity_meta_data() internal method #1 -> pass.
        """
        return True