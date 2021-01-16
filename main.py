from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, ChartParser
from equit_ease.displayer.display import QuoteDisplayer, TrendsDisplayer

import argparse
from PyInquirer import prompt, Separator


parser = argparse.ArgumentParser(description="Access stock data from the command line.")
parser.add_argument(
    "--equity", "-e", type=str, required=True, help="the equity to return data for."
)
parser.add_argument(
    "--out",
    "-o",
    type=str,
    required=False,
    help="send data printed to STDOUT to a file.",
)
parser.add_argument(
    "--force",
    "-f",
    type=str,
    default=True,
    help="If `False`, shows a list of equities matching the value passed to `--equity`. This is useful if you want to ensure that the data returned matches the equity you are searching for. If `True` (default), sends a request based off the value specified with `--equity`.",
)

args = parser.parse_args()

if __name__ == "__main__":
    reader = Reader(args.equity)
    reader.build_company_lookup_url()
    if args.force == "False":
        long_name, ticker, choices = reader.get_equity_company_data(force=args.force)
        questions = [
            {
                "type": "list",
                "name": "theme",
                "message": "Select The Correct Equity:",
                "choices": choices,
            }
        ]

        answers = prompt(questions, style=None)
    else:
        long_name, ticker = reader.get_equity_company_data(force=args.force)

    reader.ticker = ticker
    reader.name = long_name

    reader.build_equity_quote_url()
    reader.build_equity_chart_url()

    equity_quote_data = reader.get_equity_quote_data()
    equity_chart_data = reader.get_equity_chart_data()

    quote_parser = QuoteParser(equity=reader.equity, data=equity_quote_data)
    chart_parser = ChartParser(equity=reader.equity, data=equity_chart_data)
    quote_data = quote_parser.extract_equity_meta_data()
    (
        low_equity_data,
        high_equity_data,
        open_equity_data,
        close_equity_data,
        volume_equity_data,
        timestamp_data,
    ) = chart_parser.extract_equity_chart_data()

    quote_displayer = QuoteDisplayer(reader.equity, quote_data)
    table = quote_displayer.tabularize()
    for row in table:
        print(row)

    historical_displayer = TrendsDisplayer(reader)
    equity_one_year_percentage_change = historical_displayer.display_historical_price_trends("chart_one_year_url")
    equity_six_months_percentage_change = historical_displayer.display_historical_price_trends("chart_six_months_url")
    equity_three_months_percentage_change = historical_displayer.display_historical_price_trends("chart_three_months_url")
    equity_one_month_percentage_change = historical_displayer.display_historical_price_trends("chart_one_month_url")
    equity_five_days_percentage_change = historical_displayer.display_historical_price_trends("chart_five_days_url")

    # quote_contents = stringified_representation.split("\n")
    # if args.out:
    #     with open(args.out, "w") as f:
    #         f.write("\n\t".join(line  for line in quote_contents))
    # else:
    #     print("\n\t".join(line  for line in quote_contents))
