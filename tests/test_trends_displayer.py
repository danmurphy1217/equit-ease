import unittest

from equit_ease.displayer.display import TrendsDisplayer
from equit_ease.reader.read import Reader

class TestTrendsDisplayer(unittest.TestCase):
    """Testing methods from the TrendsDisplayer class."""

    def setUp(self):
        def set_up_reader_co(reader: Reader) -> Reader:
            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.build_equity_quote_url()
            reader.build_equity_chart_url()
            return reader

        def set_up_reader_tick(reader: Reader) -> Reader:
            reader.build_company_lookup_url()
            long_name, ticker = reader.get_equity_company_data(force=True)
            reader.ticker = ticker
            reader.name = long_name

            reader.build_equity_quote_url()
            reader.build_equity_chart_url()
            return reader

        self.company_name = "Apple"
        self.ticker_name = "AAPL"
        reader_co = set_up_reader_co(Reader(self.company_name))
        reader_tick = set_up_reader_tick(Reader(self.ticker_name))

        self.trends_displayer_co = TrendsDisplayer(
            reader_co
        )
        self.trends_displayer_tick = TrendsDisplayer(
            reader_tick
        )

    def tearDown(self):
        self.trends_displayer = TrendsDisplayer
    
    def test_get_percentage_change(self):
        """
        Test Case #1 for get_percentage_change() -> pass.

        test that the correct percent change is returned from
        the function with various inputs.
        """
        percent_change_pos_co = self.trends_displayer_co.get_percentage_change(
            start_value=75,
            end_value=200,
            num_decimal_places=2
        )

        percent_change_pos_tick = self.trends_displayer_tick.get_percentage_change(
            start_value=75,
            end_value=200,
            num_decimal_places=2
        )

        percent_change_negative_co = self.trends_displayer_co.get_percentage_change(
            start_value=200,
            end_value=75,
            num_decimal_places=2
        )

        percent_change_negative_tick = self.trends_displayer_tick.get_percentage_change(
            start_value=200,
            end_value=75,
            num_decimal_places=2
        )

        self.assertGreaterEqual(
            percent_change_pos_co,
            0
        )
        self.assertLessEqual(
            percent_change_negative_co,
            0
        )
        
        self.assertGreaterEqual(
            percent_change_pos_tick,
            0
        )
        self.assertLessEqual(
            percent_change_negative_tick,
            0
        )
        
