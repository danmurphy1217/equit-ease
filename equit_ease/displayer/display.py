from __future__ import annotations
import math
import os
from statistics import quantiles
import dataclasses
from typing import Any, List

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

    def _set_graph_axes(self):
        """builds the axes and core plot for the chart."""
        x_axis_range = list(range(*self.x_axes))
        y_axis_range = list(range(*self.y_axes))
        
        plot = []
        n_columns = (2*os.get_terminal_size().columns)//4
        n_rows = os.get_terminal_size().lines//2

        plot = self._build_plot(n_columns, n_rows, "-", "|")

        # return len(plot), len(plot[0])
        for line in plot:
            print(line)

    
    def build_x_axes():
        """"""

    
    def build_y_axes():
        """"""
    
    @staticmethod
    def _build_plot(x_axis: int, y_axis: int, x_axis_pattern: str, y_axis_pattern: str) -> List[List[Any]]:
        """
        build plot used to display price/volume data.

        :param x_axis -> ``int``: the number of rows
        :param y_axis -> ``int``:
        :param axes_pattern: ``str``:
        """
        plot = []
        for i in range(y_axis):
            x_axis_values = []
            for j in range(x_axis):
                if i ==  0 or i == max(range((y_axis))):
                    x_axis_values.append(x_axis_pattern)
                else:
                    if j == 0 or j == max(range(x_axis)):
                        x_axis_values.append(y_axis_pattern)
                    else:
                        x_axis_values.append(" ")
            plot.append("".join(x_axis_values))
        
        return plot


class QuoteDisplayer(Displayer):
    """contains methods used solely for the displayment of quote data."""

    def stringify(self: QuoteDisplayer) -> str:
        """
        str representation of the quote meta-data.

        :param self -> ``QuoteDisplayer``:
        """
        dataclass_as_dict = dataclasses.asdict(self.data)

        s = '''\n'''
        for key, value in dataclass_as_dict.items():
            s += self.__repr__(key, value)
        return s

    def __repr__(self, key: str, value: Any) -> str:
        """
        builds a string representation of a key-value pair of EquityMeta.

        :param key -> ``str``: a key from an EquityMeta object.
        :param value -> ``str``: a value associated with ``key``.

        :returns result -> ``str``: a string representation of the key-value pair.
        """
        formatted_key = self.set_formatting(key, "bold")
        formatted_value = self.set_formatting(value, ["color", "bold", "underline"])
        result = self.set_formatting(f"{formatted_key}: {formatted_value}\n", "align")
        return result
