from reader.read import Reader
from parser.parse import Parser

reader = Reader("F")

reader.build_equity_quote_url
reader.build_equity_chart_url

equity_quote_data = reader.get_equity_quote_data()
equity_chart_data = reader.get_equity_chart_data()

parser = Parser(equity_to_search=reader.equity_to_search, quote_data=equity_quote_data, chart_data=equity_chart_data)
parser.extract_equity_meta_data()
parser.extract_equity_chart_data()
# print(Parser.__mro__)