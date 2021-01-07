from __future__ import annotations
import os
import dataclasses
from typing import Any

from equit_ease.datatypes.equity_meta import EquityMeta
from equit_ease.parser.parse import Parser


class Displayer(Parser):
    """contains methods relating to the displayment of quote and chart data."""

    def __init__(self, equity_to_search, data):
        super().__init__(equity_to_search, data)

    @staticmethod
    def center_print(string_to_print: str) -> None:
        """
        center prints a string to the console.

        :param string_to_print -> ``str``: the string to print to the console.
        :returns ``None``:
        """
        terminal_width, _ = os.get_terminal_size()
        print(f"{string_to_print}".center(terminal_width))


class ChartDisplayer(Displayer):
    """"contains methods used solely for the displayment of the chart data."""


class QuoteDisplayer(Displayer):
    """contains methods used solely for the displayment of quote data."""

    def stringify(self: QuoteDisplayer) -> str:
        """
        str representation of the quote meta-data. This is printed
        to the console with self.center_print().

        :param self -> ``QuoteDisplayer``:
        """
        dataclass_as_dict = dataclasses.asdict(self.data)

        s = '''\n'''
        for key, value in dataclass_as_dict.items():
            s += self.__repr__(key, value)
        return s

    @staticmethod    
    def __repr__(key: str, value: Any) -> str:
        """
        builds a string representation of a key-value pair of EquityMeta.

        :param key -> ``str``: a key from an EquityMeta object.
        :param value -> ``str``: a value associated with ``key``.

        :returns result -> ``str``: a string representation of the key-value pair.
        """
        return f"{key}: {value}\n"
