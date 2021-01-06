class Constants:
    """Dedicated to storing any constants used throughout this program in a centralized location."""

    yahoo_finance_base_chart_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    yahoo_finance_base_quote_url = "https://query1.finance.yahoo.com/v7/finance/quote"
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
    # https://query1.finance.yahoo.com/v8/finance/chart/T?region=US&lang=en-US&includePrePost=false&interval=1d&range=6mo
