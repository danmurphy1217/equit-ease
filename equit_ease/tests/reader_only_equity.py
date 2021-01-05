import unittest
from equit_ease.reader.read import Reader
from equit_ease.utils.Constants import Constants


class TestReaderMethodsOnly(unittest.TestCase):
    # test the methods defined for the Reader class.

    def test_build_equity_url_for_pass(self):
        """test case #1 for build_equity_url_for() in reader/read.py -> pass"""
        ticker_to_search = "tsla"
        reader = Reader(ticker_to_search)
        reader_upper = Reader(ticker_to_search.upper())
        
        full_url_one = Constants.yahoo_finance_base_chart_url + ticker_to_search
        # builds the URL and sets it as a class instance(!!!) attribute
        _ = reader.build_equity_url
        self.assertEqual(reader.url, full_url_one)
        
        full_url_two = Constants.yahoo_finance_base_chart_url + ticker_to_search.upper()
        _ = reader_upper.build_equity_url
        self.assertEqual(reader_upper.url, full_url_two)
        
        _ = reader_upper.build_equity_url
        self.assertNotEqual(reader_upper.url, full_url_one)

    def test_build_url_for_fail(self):
        """test case #2 for build_equity_url_for() in reader/read.py -> throw error"""
        ticker_to_search = "XYZ"
        with self.assertRaises(ValueError):
            reader = Reader(ticker_to_search)
            reader.build_equity_url
