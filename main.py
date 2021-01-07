from equit_ease.reader.read import Reader
from equit_ease.parser.parse import QuoteParser, ChartParser
from equit_ease.displayer.display import Displayer, QuoteDisplayer, ChartDisplayer

from pyfiglet import Figlet
import os

fig = Figlet()
reader = Reader("MSFT")
reader.build_equity_quote_url
reader.build_equity_chart_url
equity_quote_data = reader.get_equity_quote_data()
equity_chart_data = reader.get_equity_chart_data()

quote_parser = QuoteParser(equity_to_search=reader.equity_to_search, data=equity_quote_data)
chart_parser = ChartParser(equity_to_search=reader.equity_to_search, data=equity_chart_data)
quote_data = quote_parser.extract_equity_meta_data()
chart_data = chart_parser.extract_equity_chart_data()

title = fig.renderText(reader.equity_to_search)
displayer = QuoteDisplayer(reader.equity_to_search, quote_data)
stringified_representation = displayer.stringify()
quote_contents = stringified_representation.split("\n")
[print(line.center(os.get_terminal_size().columns)) for line in title.split("\n")]
print("\n\t".join(line  for line in quote_contents))
