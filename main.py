from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, ChartParser
from equit_ease.displayer.display import QuoteDisplayer, TrendsDisplayer

import argparse
from PyInquirer import prompt, Separator
import os
from pathlib import Path
import re

parser = argparse.ArgumentParser(description="The easiest way to access stock market data from the command line.")
parser.add_argument(
    "config",
    type=str,
    nargs="?",
    help="create lists of stocks for seamless future retrieval." 
)
parser.add_argument(
    "--equity", 
    "-e",
    type=str,
    help="the equity to retrieve data for."
)
parser.add_argument(
    "--force",
    "-f",
    type=str,
    default=True,
    help="If `False`, shows a list of equities matching the value passed to `--equity`. This is useful if you want to ensure that the data returned matches the equity you are searching for. If `True` (default), sends a request based off the value specified with `--equity`.",
)
parser.add_argument(
    "--list", 
    "-l",
    type=str,
    help="the equity to retrieve data for."
)

args = parser.parse_args()

if __name__ == "__main__":
    if args.config:
       questions = [
           {
               "type": "input",
               "name": "list_name",
               "message": "List Name:"
            },
           {
               "type": "input",
               "name": "equities_in_list",
               "message": "Equities to include in list:"
            },

        ]
       answers = prompt(questions, style=None)
       user_home_dir = os.environ.get("HOME")
       equit_ease_dir_path = os.path.join(user_home_dir, ".equit_ease")
       os_agnostic_path = Path(equit_ease_dir_path)
       config_file_path = Path(os.path.join(equit_ease_dir_path, "lists"))

       if not os.path.exists(os_agnostic_path):
           os_agnostic_path.mkdir() # create .equit_ease dir in $HOME
           config_file_path.touch() # create config file
           with open(config_file_path, "w") as f:
               init_list_name = answers["list_name"]
               cleaner = lambda equity_names_list: [name.strip() for name in equity_names_list]
               equity_names = answers["equities_in_list"]
               equity_names_formatted = ",".join(cleaner(equity_names.split(",")))

               contents_for_file = f'''[{init_list_name}]\nequity_names = {equity_names_formatted}'''
               f.write(contents_for_file)
       else:
           with open(config_file_path, "a") as f:
               cleaner = lambda equity_names_list: [name.strip() for name in equity_names_list]
               list_name = answers["list_name"]
               equity_names = answers["equities_in_list"]
               equity_names_formatted = ",".join(cleaner(equity_names.split(",")))
               contents_for_file = f'''\n[{list_name}]\nequity_names = {equity_names_formatted}'''
               f.write(contents_for_file)
    elif args.equity:
        reader = Reader(args.equity)
        reader.build_company_lookup_url()
        if args.force == "False":
            long_name, ticker, choices = reader.get_equity_company_data(force=args.force)
            questions = [
                {
                    "type": "list",
                    "name": "Equity_Name",
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

        quote_displayer = QuoteDisplayer(reader.equity, quote_data)
        table = quote_displayer.tabularize()

        trends_displayer = TrendsDisplayer(reader)
        equity_one_year_percentage_change = trends_displayer.build_historical_price_trends("chart_one_year_url")
        equity_six_months_percentage_change = trends_displayer.build_historical_price_trends("chart_six_months_url")
        equity_three_months_percentage_change = trends_displayer.build_historical_price_trends("chart_three_months_url")
        equity_one_month_percentage_change = trends_displayer.build_historical_price_trends("chart_one_month_url")
        equity_five_days_percentage_change = trends_displayer.build_historical_price_trends("chart_five_days_url")

        for row in table:
            print(row)

        print(f"\n{reader.ticker} is:\n")

        trends_displayer.display(equity_one_year_percentage_change, "year")
        trends_displayer.display(equity_six_months_percentage_change, "6 months")
        trends_displayer.display(equity_three_months_percentage_change, "3 months")
        trends_displayer.display(equity_one_month_percentage_change, "1 month")
        trends_displayer.display(equity_five_days_percentage_change, "1 week")

        # quote_contents = stringified_representation.split("\n")
        # if args.out:
        #     with open(args.out, "w") as f:
        #         f.write("\n\t".join(line  for line in quote_contents))
        # else:
        #     print("\n\t".join(line  for line in quote_contents))
    elif args.list:
        list_name = args.list
        user_home_dir = os.environ.get("HOME")
        equit_ease_dir_path = os.path.join(user_home_dir, ".equit_ease")
        config_file_path = Path(os.path.join(equit_ease_dir_path, "lists"))
        with open(config_file_path, "r") as f:
            file_contents_lines = f.read().splitlines()
        
        for i, line in enumerate(file_contents_lines):
            if re.search(rf"{list_name}(?=])", line):
                equity_names_to_search_unformatted = file_contents_lines[i + 1]
                equity_names_to_search_formatted = equity_names_to_search_unformatted.split(" = ")[-1]
                #TODO: ensure that input is stripped of any spaces: AAPL,CRM,MSFT,CRWD
                split_names = lambda name : name.split(",")
                equities_to_search = split_names(equity_names_to_search_formatted)

                for equity in equities_to_search:
                    reader = Reader(equity)
                    reader.build_company_lookup_url()
                    if args.force == "False":
                        long_name, ticker, choices = reader.get_equity_company_data(force=args.force)
                        questions = [
                            {
                                "type": "list",
                                "name": "Equity_Name",
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

                    quote_displayer = QuoteDisplayer(reader.equity, quote_data)
                    table = quote_displayer.tabularize()

                    trends_displayer = TrendsDisplayer(reader)
                    equity_one_year_percentage_change = trends_displayer.build_historical_price_trends("chart_one_year_url")
                    equity_six_months_percentage_change = trends_displayer.build_historical_price_trends("chart_six_months_url")
                    equity_three_months_percentage_change = trends_displayer.build_historical_price_trends("chart_three_months_url")
                    equity_one_month_percentage_change = trends_displayer.build_historical_price_trends("chart_one_month_url")
                    equity_five_days_percentage_change = trends_displayer.build_historical_price_trends("chart_five_days_url")

                    for row in table:
                        print(row)

                    print(f"\n{reader.ticker} is:\n")

                    trends_displayer.display(equity_one_year_percentage_change, "year")
                    trends_displayer.display(equity_six_months_percentage_change, "6 months")
                    trends_displayer.display(equity_three_months_percentage_change, "3 months")
                    trends_displayer.display(equity_one_month_percentage_change, "1 month")
                    trends_displayer.display(equity_five_days_percentage_change, "1 week")
            else:
                pass
        # with open(config_file_path)