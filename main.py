from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, ChartParser
from equit_ease.displayer.display import Displayer, QuoteDisplayer, ChartDisplayer

from pyfiglet import Figlet
import os

fig = Figlet()
reader = Reader("CRM")
reader.build_company_lookup_url()
long_name, ticker = reader.get_equity_company_data()
reader.ticker = ticker
reader.name = long_name

print(reader.ticker, " | ", reader.name)

reader.build_equity_quote_url()
reader.build_equity_chart_url()

equity_quote_data = reader.get_equity_quote_data()
equity_chart_data = reader.get_equity_chart_data()

quote_parser = QuoteParser(equity=reader.equity, data=equity_quote_data)
chart_parser = ChartParser(equity=reader.equity, data=equity_chart_data)
quote_data = quote_parser.extract_equity_meta_data()
low_equity_data, high_equity_data, open_equity_data, close_equity_data, volume_equity_data = chart_parser.extract_equity_chart_data()

# title = fig.renderText(reader.name)
# displayer = QuoteDisplayer(reader.equity, quote_data)
# stringified_representation = displayer.stringify()
# quote_contents = stringified_representation.split("\n")
# [print(line.center(os.get_terminal_size().columns)) for line in title.split("\n")]
# print("\n\t".join(line  for line in quote_contents))

print(min(low_equity_data), max(high_equity_data))
