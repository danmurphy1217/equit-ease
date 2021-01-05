from equit_ease.reader.read import Reader

class Parser(Reader):
    def __init__(self, ticker_symbol):
        super().__init__(ticker_symbol)