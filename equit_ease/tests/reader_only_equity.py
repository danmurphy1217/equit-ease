import unittest
from equit_ease.reader.read import Reader
from equit_ease.utils.Constants import Constants


class TestReaderMethods(unittest.TestCase):
    # test the methods defined for the Reader class.

    def test_build_equity_chart_url_for_pass(self):
        """test case #1 for build_equity_chart_url() in reader/read.py -> pass"""
        ticker_to_search = "tsla"
        reader = Reader(ticker_to_search)
        reader_upper = Reader(ticker_to_search.upper())
        
        full_url_one = Constants.yahoo_finance_base_chart_url + ticker_to_search
        # builds the URL and sets it as a class instance(!!!) attribute
        _ = reader.build_equity_chart_url
        self.assertEqual(reader.chart_url, full_url_one)
        
        full_url_two = Constants.yahoo_finance_base_chart_url + ticker_to_search.upper()
        _ = reader_upper.build_equity_chart_url
        self.assertEqual(reader_upper.chart_url, full_url_two)
        
        _ = reader_upper.build_equity_chart_url
        self.assertNotEqual(reader_upper.chart_url, full_url_one)

    def test_build_url_for_fail(self):
        """test case #2 for build_equity_url_for() in reader/read.py -> throw error"""
        ticker_to_search = "XYZ"
        with self.assertRaises(ValueError):
            reader = Reader(ticker_to_search)
            reader.build_equity_chart_url
    
    def test_get_equity_chart_data_pass(self):
        """test case #1 for get_equity_chart_data() in reader/read.py -> pass"""
        ticker_to_search = "TSLA"
        reader = Reader(ticker_to_search)
        reader.build_equity_chart_url

        equity_data = reader.get_equity_chart_data()

        # check some of the response data...
        self.assertEqual(list(equity_data.keys()), ['chart'])
        self.assertTrue(('result' and 'error') in equity_data['chart'].keys())
        self.assertTrue(( 'meta' and 'timestamp' and 'indicators') in equity_data['chart']['result'][0].keys())
        self.assertIsNone(equity_data['chart']['error'])

    
    # def test_get_equity_data_fail():
    #     """test case #2 for get_equity_chart_data() in reader/read.py -> fail"""
    #     return

    def test_get_equity_quote_data_pass(self):
        """test case #1 for get_equity_quote_data()"""