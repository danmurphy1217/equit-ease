import PyInquirer
from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, ChartParser
from equit_ease.displayer.display import QuoteDisplayer, TrendsDisplayer

import argparse
from PyInquirer import prompt
import os
from pathlib import Path
import re
from typing import Dict
def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    instantiate the parser object with the necessary arguments.

    :param parser -> ``argparse.ArgumentParser``: a parser object with no arguments added.
    
    :returns parser -> ``argparse.ArgumentParser``: a parser object containing the needed arguments.
    """
    parser.add_argument(
        "config",
        type=str,
        nargs="?",
        help="create a named list of stocks that can easily be retrieved later with the ``--list`` or ``-l`` flag.",
    )
    
    parser.add_argument(
        "--force",
        "-f",
        type=str,
        default=True,
        help="If `False`, shows a list of all equities returned from the reverse lookup and lets you choose which one to retrieve data for. This is useful if you want to ensure that the data returned matches the equity you truly want to search for. If `True` (default), sends a request matching the first ticker returned from the reverse lookup.",
    )
    
    parser.add_argument("--equity", "-e", type=str, help="the equity to retrieve data for.")
    parser.add_argument("--list", "-l", type=str, help="the equity to retrieve data for.")

    return parser

class ArgsHandler:

    def __init__(self, args_data: argparse.Namespace):
        self.args_data = args_data

    def handle_config(self):
        """
        the `config` positional arg takes precedence over other args. If config
        exists in the args, then that is the process that is initiated and handled.

        :param self -> ``ArgsHandler``:

        :returns ``??``: # FIXME
        """
        questions = [
            {"type": "input", "name": "list_name", "message": "List Name:"},
            {
                "type": "input",
                "name": "equities_in_list",
                "message": "Equities to include in list:",
            },
        ]
        answers = prompt(questions, style=None)

        user_home_dir = os.environ.get("HOME")
        equit_ease_dir_path = os.path.join(user_home_dir, ".equit_ease")
        os_agnostic_path = Path(equit_ease_dir_path)
        config_file_path = Path(os.path.join(equit_ease_dir_path, "lists"))

        if not os.path.exists(os_agnostic_path):
            self._make_dir_and_lists_file(os_agnostic_path, config_file_path, answers)
        else:
            self._append_to_lists_file(config_file_path, answers)
    
    def handle_equity(self):
        """
        if the ``--equity`` or ``-e`` flags are specified, the equity name that
        is provided is used to perform a reverse lookup. The first result from that
        lookup is then used to retrieve data and print it to the console.

        If ``--force`` or ``-f`` is set to `False`, then you are given the flexibility
        of choosing the correct equity from the reverse lookup. This is useful is you
        do not know the exact ticker and want to ensure the correct equity is searched
        for.
        """
        # FIXME: re-locate and re-factor code from args.equity here.
    @staticmethod
    def _make_dir_and_lists_file(dir_path: Path, list_file_path: Path, answers: PyInquirer.prompt) -> bool:
        """
        make .equit_ease folder in $HOME dir.

        :params dir_path -> ``Path``: a Path object representing an operating system-agnostic path
                                  (works on POSIX and Windows)
        :params list_file_path -> ``Path``: file path for the lists ASCII text file.
        :param answers -> ``PyInquirer.prompt``: answers to the prompt.
        
        :returns True -> ``bool``:
        """
        dir_path.mkdir()  # create .equit_ease dir in $HOME
        list_file_path.touch()  # create config file
        with open(list_file_path, "w") as f:
            init_list_name = answers["list_name"]
            cleaner = lambda equity_names_list: [
                name.strip() for name in equity_names_list
            ]
            equity_names = answers["equities_in_list"]
            equity_names_formatted = ",".join(cleaner(equity_names.split(",")))

            contents_for_file = (
                f"""[{init_list_name}]\nequity_names = {equity_names_formatted}"""
            )
            f.write(contents_for_file)     
    
    @staticmethod
    def _append_to_lists_file(lists_file_path: Path, answers: PyInquirer.prompt) -> bool:
        """
        if the .equit_ease dir already exists, then append to the
        lists ASCII text file in the directory (this file is created 
        when the dir is created, so it is expected to already exist).

        :params lists_file_path -> ``Path``: the path to the `lists` ASCII text file.
        :param answers -> ``PyInquirer.prompt``: answers to the prompt.

        :returns True -> ``bool``:
        """
        with open(lists_file_path, "a") as f:
            cleaner = lambda equity_names_list: [
                name.strip() for name in equity_names_list
            ]
            list_name = answers["list_name"]
            equity_names = answers["equities_in_list"]
            equity_names_formatted = ",".join(cleaner(equity_names.split(",")))
            contents_for_file = (
                f"""\n[{list_name}]\nequity_names = {equity_names_formatted}"""
            )
            f.write(contents_for_file)

parser = argparse.ArgumentParser(
    description="The easiest way to access data about your favorite stocks from the command line."
)
parser = init_parser(parser=parser)
args = parser.parse_args()

if __name__ == "__main__":
    if args.config:
        args_handler = ArgsHandler(args)
        print(args_handler.args_data)
        args_handler.handle_config()

    elif args.equity:
        reader = Reader(args.equity)
        reader.build_company_lookup_url()
        if args.force == "False":
            long_name, ticker, choices = reader.get_equity_company_data(
                force=args.force
            )
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
        equity_one_year_percentage_change = (
            trends_displayer.build_historical_price_trends("chart_one_year_url")
        )
        equity_six_months_percentage_change = (
            trends_displayer.build_historical_price_trends("chart_six_months_url")
        )
        equity_three_months_percentage_change = (
            trends_displayer.build_historical_price_trends("chart_three_months_url")
        )
        equity_one_month_percentage_change = (
            trends_displayer.build_historical_price_trends("chart_one_month_url")
        )
        equity_five_days_percentage_change = (
            trends_displayer.build_historical_price_trends("chart_five_days_url")
        )

        for row in table:
            print(row)

        print(f"\n{reader.ticker} is:\n")

        trends_displayer.display(equity_one_year_percentage_change, "year")
        trends_displayer.display(equity_six_months_percentage_change, "6 months")
        trends_displayer.display(equity_three_months_percentage_change, "3 months")
        trends_displayer.display(equity_one_month_percentage_change, "1 month")
        trends_displayer.display(equity_five_days_percentage_change, "1 week")

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
                equity_names_to_search_formatted = (
                    equity_names_to_search_unformatted.split(" = ")[-1]
                )
                # TODO: ensure that input is stripped of any spaces: AAPL,CRM,MSFT,CRWD
                split_names = lambda name: name.split(",")
                equities_to_search = split_names(equity_names_to_search_formatted)

                for equity in equities_to_search:
                    reader = Reader(equity)
                    reader.build_company_lookup_url()
                    if args.force == "False":
                        long_name, ticker, choices = reader.get_equity_company_data(
                            force=args.force
                        )
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
                        long_name, ticker = reader.get_equity_company_data(
                            force=args.force
                        )

                    reader.ticker = ticker
                    reader.name = long_name

                    reader.build_equity_quote_url()
                    reader.build_equity_chart_url()

                    equity_quote_data = reader.get_equity_quote_data()
                    equity_chart_data = reader.get_equity_chart_data()

                    quote_parser = QuoteParser(
                        equity=reader.equity, data=equity_quote_data
                    )
                    chart_parser = ChartParser(
                        equity=reader.equity, data=equity_chart_data
                    )
                    quote_data = quote_parser.extract_equity_meta_data()

                    quote_displayer = QuoteDisplayer(reader.equity, quote_data)
                    table = quote_displayer.tabularize()

                    trends_displayer = TrendsDisplayer(reader)
                    equity_one_year_percentage_change = (
                        trends_displayer.build_historical_price_trends(
                            "chart_one_year_url"
                        )
                    )
                    equity_six_months_percentage_change = (
                        trends_displayer.build_historical_price_trends(
                            "chart_six_months_url"
                        )
                    )
                    equity_three_months_percentage_change = (
                        trends_displayer.build_historical_price_trends(
                            "chart_three_months_url"
                        )
                    )
                    equity_one_month_percentage_change = (
                        trends_displayer.build_historical_price_trends(
                            "chart_one_month_url"
                        )
                    )
                    equity_five_days_percentage_change = (
                        trends_displayer.build_historical_price_trends(
                            "chart_five_days_url"
                        )
                    )

                    for row in table:
                        print(row)

                    print(f"\n{reader.ticker} is:\n")

                    trends_displayer.display(equity_one_year_percentage_change, "year")
                    trends_displayer.display(
                        equity_six_months_percentage_change, "6 months"
                    )
                    trends_displayer.display(
                        equity_three_months_percentage_change, "3 months"
                    )
                    trends_displayer.display(
                        equity_one_month_percentage_change, "1 month"
                    )
                    trends_displayer.display(
                        equity_five_days_percentage_change, "1 week"
                    )
            else:
                pass
        # with open(config_file_path)
