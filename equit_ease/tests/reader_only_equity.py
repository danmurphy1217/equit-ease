import unittest 
from equit_ease.reader.read import Reader
from equit_ease.utils.Constants import Constants


class TestReaderMethodsOnly(unittest.TestCase):
    # test the methods defined for the Reader class.

    def test_build_equity_url_for_pass(self):
        """test case #1 for build_equity_url_for() in reader/read -> pass"""
        ticker_to_search = "tsla"
        reader = Reader(ticker_to_search)
        assert reader.build_equity_url_for() == Constants.yahoo_finance_base_chart_url + ticker_to_search

