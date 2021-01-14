from __future__ import annotations
from datetime import datetime
import os
import dataclasses
from typing import Any, List, Tuple, Set

from requests.api import head

from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.parser.parse import Parser
from equit_ease.displayer.format import Formatter
from equit_ease.utils.Constants import Constants


class Displayer(Parser):
    """contains methods relating to the displayment of quote and chart data."""

    def __init__(self, equity_to_search, data):
        super().__init__(equity_to_search, data)

    def set_formatting(self, value_to_format: str or int, formatting_type: str) -> str:
        """
        apply a template of formatting to the provided value.

        :param value_to_format -> ``str``: the value that should be formatted.
        :param formatting_type -> ``str``: the type of formatting to perform.
        :return result -> ``str``: the result to return.
        """
        result = value_to_format

        # https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
        if isinstance(formatting_type, list):
            for styling in formatting_type:
                result = Constants.dispatcher[styling](result)
        else:
            result = Constants.dispatcher[formatting_type](result)

        return result


class ChartDisplayer(Displayer):
    """"contains methods used solely for the displayment of the chart data."""

    def __init__(self, x_axes, y_axes, title):
        self.x_axes = x_axes
        self.y_axes = y_axes
        self.title = title
    

class QuoteDisplayer(Displayer):
    """contains methods used solely for the displayment of quote data."""

    def tabularize(self: QuoteDisplayer) -> str:
        """
        str representation of the quote meta-data.

        :param self -> ``QuoteDisplayer``:
        """
        dataclass_as_dict = dataclasses.asdict(self.data)

        row_one = []
        row_two = []
        padding_sizes = []

        for key, value in dataclass_as_dict.items():
            if key in Constants.default_display_data:
                
                max_padding = len(key) if len(key) > len(str(value)) else len(str(value))
                row_one.append(key), row_two.append(value)
                padding_sizes.append(max_padding)


        return self._build_table(padding_sizes, rows=[row_one]), self._build_table(padding_sizes, rows=[row_two])
    
    def _build_table(self: QuoteDisplayer, padding_size: List[int], **kwargs):

        def build_rows():
            return
        
        def build_row_separators(row: List[str]):
            """
            build the separators that exist between each row.

            :param row -> ``List[str]``: the row used to determine the length of the separator.
            :returns result -> ``str``: a string len(row) long used as the separator.
            """
            result = "-"*(len(row))
            return result
            
        r = " | "
        rows = kwargs['rows']
        
        for row in rows:
            for i, item in enumerate(row):
                padding = padding_size[i]
                r += " "*(padding - len(str(item))) + str(item) + " | "
            return build_row_separators(r), r
    

    def __repr__(self, key: str, value: Any) -> str:
        """
        builds a string representation of a key-value pair of EquityMeta.

        :param key -> ``str``: a key from an EquityMeta object.
        :param value -> ``str``: a value associated with ``key``.

        :returns result -> ``str``: a string representation of the key-value pair.
        """
        formatted_key = self.set_formatting(key, ["split", "capitalize", "bold"])
        formatted_value = self.set_formatting(value, ["color", "bold", "underline"])
        result = self.set_formatting(f"{formatted_key}: {formatted_value}\n", "align")
        return result
