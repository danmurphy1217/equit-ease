import unittest
from requests.exceptions import HTTPError

from equit_ease.reader.read import Reader
from equit_ease.utils.Constants import Constants


class TestReaderMethods(unittest.TestCase):
    # test the methods defined for the Reader class.

    def setUp(self):
        """set-up before each test is run."""
        self.company_name = "Apple"
        self.ticker_name = "CRM"
        self.reader_co = Reader(self.company_name)
        self.reader_tick = Reader(self.ticker_name)

    def tearDown(self):
        self.company_name = None
        self.ticker_name = None
        self.reader_co = Reader
        self.reader_tick = Reader

    def test_build_equity_chart_url_pass(self):
        """test case #1 for build_equity_chart_url() in reader/read.py -> pass"""
        ticker_to_search = "Apple"

        reader = Reader("Apple")
        reader.build_company_lookup_url()
        long_name, ticker = reader.get_equity_company_data()
        reader.ticker = ticker
        reader.name = long_name

        reader.build_equity_quote_url()
        reader.build_equity_chart_url()

        full_url_one = Constants.yahoo_finance_base_chart_url + reader.ticker
        # builds the URL and sets it as a class instance(!!!) attribute
        _ = reader.build_equity_chart_url()
        self.assertEqual(reader.chart_url, full_url_one)

    # def test_build_chart_url_fail(self):
    #     """test case #2 for build_equity_url_for() in reader/read.py -> throw error"""
    #     ticker_to_search = "XYZ"
    #     with self.assertRaises(ValueError):
    #         reader = Reader(ticker_to_search)
    #         reader.build_equity_chart_url

    # def test_get_equity_chart_data_pass(self):
    #     """test case #1 for get_equity_chart_data() in reader/read.py -> pass"""
    #     ticker_to_search = "TSLA"
    #     reader = Reader(ticker_to_search)
    #     reader.build_equity_chart_url

    #     equity_chart_data = reader.get_equity_chart_data()

    #     # check some of the response data...
    #     self.assertEqual(list(equity_chart_data.keys()), ["chart"])
    #     self.assertTrue(("result" and "error") in equity_chart_data["chart"].keys())
    #     self.assertTrue(
    #         ("meta" and "timestamp" and "indicators")
    #         in equity_chart_data["chart"]["result"][0].keys()
    #     )
    #     self.assertIsNone(equity_chart_data["chart"]["error"])

    # def test_get_equity_chart_data_fail(self):
    #     """test case #2 for get_equity_chart_data() in reader/read.py -> throw error"""
    #     ticker_to_search = "XYZ"
    #     with self.assertRaises(ValueError):
    #         reader = Reader(ticker_to_search)
    #         reader.build_equity_chart_url

    #         # shouldn't reach here, error is raised immediately
    #         # after an incorrect equity ticker symbol is passed
    #         reader.get_equity_chart_data()

    # def test_get_equity_quote_data_pass(self):
    #     """test case #1 for get_equity_quote_data() -> pass"""
    #     ticker_to_search = "TSLA"
    #     reader = Reader(ticker_to_search)
    #     reader.build_equity_quote_url

    #     equity_quote_data = reader.get_equity_quote_data()

    #     # check some of the response data
    #     self.assertEqual(list(equity_quote_data.keys()), ["quoteResponse"])
    #     self.assertTrue(
    #         ("result" and "error") in equity_quote_data["quoteResponse"].keys()
    #     )
    #     self.assertTrue(
    #         (
    #             "regularMarketPreviousClose"
    #             and "regularMarketPreviousOpen"
    #             and "regularMarketVolume"
    #             and "regularMarketDayLow"
    #             and "regularMarketDayHigh"
    #             and "fiftyDayAverage"
    #             and "bid"
    #             and "ask"
    #         )
    #         in equity_quote_data["quoteResponse"]["result"][0].keys()
    #     )
    #     self.assertIsNone(equity_quote_data["quoteResponse"]["error"])

    # def test_get_equity_quote_data_fail(self):
    #     """test case #2 for get_equity_quote_data() -> throw error"""
    #     ticker_to_search = "XYZ"
    #     with self.assertRaises(ValueError):
    #         reader = Reader(ticker_to_search)
    #         reader.build_equity_quote_url

    #         reader.get_equity_quote_data()

    # def test_private_get_pass(self):
    #     """test case #1 for call private method directly -> pass."""
    #     ticker_to_search = "TSLA"
    #     reader = Reader(ticker_to_search)

    #     chart_data_response = reader._get(
    #         Constants.yahoo_finance_base_chart_url + ticker_to_search
    #     )

    #     self.assertTrue(chart_data_response["chart"]["error"] is None)
    #     self.assertTrue(
    #         ("meta" and "timestamp" and "indicators")
    #         in chart_data_response["chart"]["result"][0].keys()
    #     )

    # def test_private_get_fail(self):
    #     """
    #     test case #2 for call private method directly -> fail.

    #     this should never happen, since a validity check is sent upon initialization to
    #     ensure that a ticker symbol exists in the database. But, if the private method
    #     were to be called directly, raise_for_status() will catch it [assuming yfinance
    #     responsds with a 404].
    #     """
    #     ticker_to_search = "XYZ"
    #     reader = Reader(ticker_to_search)

    #     with self.assertRaises(HTTPError):
    #         reader._get(Constants.yahoo_finance_base_chart_url + ticker_to_search)
        
    # # def test_get_equity_company_data(self):
    # #     """
    # #     test case #1 for get_equity_company_data() -> pass.

    # #     test the get_equity_company_data() method which uses the value passed
    # #     upon initialization of the ``Reader`` class to ping Yahoo
    # #     Finance's backend and render a list of possible equities.
    # #     If no values are returned, a ``ValueError`` is thrown.
    # #     """
    # #     reader = Reader("Apple")
    # #     print(reader.get_equity_company_data())