from equit_ease.displayer.format import Formatter

class Constants:
    """Dedicated to storing any constants used throughout this program in a centralized location."""

    yahoo_finance_base_chart_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    yahoo_finance_base_quote_url = "https://query1.finance.yahoo.com/v7/finance/quote"
    yahoo_finance_co_lookup = "https://query2.finance.yahoo.com/v1/finance/search?q="

    yahoo_finance_quote_keys = [
        "regularMarketPreviousClose",
        "regularMarketOpen",
        "bid",
        "ask",
        "regularMarketDayRange",
        "fiftyTwoWeekRange",
        "regularMarketVolume",
        "averageDailyVolume3Month",
        "averageDailyVolume10Day",
        "marketCap",
        "trailingPE",
        "forwardPE",
        "epsTrailingTwelveMonths",
        "earningsTimestamp",
        "trailingAnnualDividendRate",
        "trailingAnnualDividendYield",
        "dividendDate",
    ]

    dispatcher = {
        'bold': Formatter.bold,
        'color': Formatter.set_color_for,
        'underline': Formatter.underline,
        "align": Formatter.align
    }

    # intermediary data struct used to map yahoo finance columns -> dataclass names.
    yahoo_finance_column_mappings = {
        "previous_close": "regularMarketPreviousClose",
        "open": "regularMarketOpen",
        "bid": "bid",
        "ask": "ask",
        "intra_day_range": "regularMarketDayRange",
        "fifty_two_wk_range": "fiftyTwoWeekRange",
        "market_volume": "regularMarketVolume",
        "market_three_month_volume": "averageDailyVolume3Month",
        "market_ten_day_volume": "averageDailyVolume10Day",
        "market_cap": "marketCap",
        "trailing_pe": "trailingPE",
        "forward_pe": "forwardPE",
        "trailing_eps": "epsTrailingTwelveMonths",
        "earnings_report_date": "earningsTimestamp",
        "dividend_rate": "trailingAnnualDividendRate",
        "dividend_yield": "trailingAnnualDividendYield",
        "next_dividend_date": "dividendDate",
    }

    # https://query1.finance.yahoo.com/v8/finance/chart/T?region=US&lang=en-US&includePrePost=false&interval=1d&range=6mo
