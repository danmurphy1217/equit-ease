from __future__ import annotations
from datetime import datetime
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
        
        plot = []
        n_columns = (3*os.get_terminal_size().columns) // 4
        n_rows = (os.get_terminal_size().lines) // 2

        x_axis_labels = self._build_x_axis_labels(n_columns, range(n_columns)[0], range(n_columns)[len(range(n_columns))//4], range(n_columns)[len(range(n_columns))//2], range(n_columns)[(3*len(range(n_columns)))//4], range(n_columns)[len(range(n_columns)) - 1])
        y_axis_labels = self._build_y_axis_labels(n_rows, range(n_rows)[0], range(n_rows)[len(range(n_rows))//4], range(n_rows)[len(range(n_rows))//2], range(n_rows)[(3*len(range(n_rows)))//4], range(n_rows)[len(range(n_rows)) - 1])[::-1]
        padded_y_axis_labels = self._set_padding(y_axis_labels)
        max_width = len(max(y_axis_labels, key=len))
        padded_x_axis_labels = max_width*" " + x_axis_labels
        
        plot = self._build_plot(len(x_axis_labels), n_rows, "_", "|")
        plot.append(padded_x_axis_labels)

        for i, line in enumerate(plot):
            if isinstance(line, list):
                line.insert(0, padded_y_axis_labels[i])
            print("".join(line))

    def _build_x_axis_labels(self, n_columns: int, *args: str) -> str:
        """
        build x axis labels for the plot.

        :param n_columns -> ``int``: the number of columns in the plot.
        :args -> ``str``: should contain the indices on which the labels should be placed.

        :returns result -> ``str``: a formatted list of x-axis labels
        """
        labels = [" "]*n_columns
        axes_len = len(self.x_axes)
        min = self.x_axes[0]
        q_one = self.x_axes[axes_len // 4]
        q_two = self.x_axes[axes_len // 2]
        q_three = self.x_axes[ (3*axes_len) // 4]
        max = self.x_axes[axes_len - 1]
        l = [min, q_one, q_two, q_three, max]

        for i, arg in enumerate(args):
            labels[arg] = datetime.fromtimestamp(l[i]).strftime("%H")
        
        return "".join(labels)


    
    def _build_y_axis_labels(self, n_rows: int, *args: str) -> str:
        """
        build y axis for the plot.
        
        :param n_rows: -> the number of rows in the plot.
        :args -> ``str``: should contain the indices on which the labels should be placed.
        """
        labels = [" "]*n_rows
        axes_len = len(self.y_axes)
        min = sorted(self.y_axes)[0]
        q_one = sorted(self.y_axes)[axes_len // 4]
        q_two = sorted(self.y_axes)[axes_len // 2]
        q_three = sorted(self.y_axes)[ (3*axes_len) // 4]
        max = sorted(self.y_axes)[axes_len - 1]
        l = [min, q_one, q_two, q_three, max]

        for i, arg in enumerate(args):
            labels[arg] = str(l[i])
        
        return labels

    @staticmethod
    def _set_padding(labels: List[str]):
        """
        adds whitespace along the y-axis to align labels.
        
        :param labels -> ``List[str]``: the labels for the y axis of the plot.

        :returns result -> ``List[str]``:  padded y axis labels.
        """
        max_width = len(max(labels, key=len))
        padded_labels = []

        for label in labels:
            label_length_diff = max_width - len(label)
            padding = " "*label_length_diff
            padded_label = padding + label + " "
            padded_labels.append(padded_label)
        
        return padded_labels


    
    @staticmethod
    def _build_plot(x_axis: int, y_axis: int, x_axis_pattern: str, y_axis_pattern: str) -> List[List[str]]:
        """
        build plot used to display price/volume data.

        :param x_axis -> ``int``: the number of columns for the plot
        :param y_axis -> ``int``: the number of lines for the plot
        :param x_axis_pattern: ``str``: the pattern to use for drawing the x axis
        :param y_axis_pattern: ``str``: the pattern to use for drawing the y axis

        :returns plot -> ``List[str]``: the plot represented as a one-dimensional array.
        """
        plot = []
        for i in range(y_axis):
            x_axis_values = []
            for j in range(x_axis):
                if i ==  0 or i == max(range(y_axis)):
                    x_axis_values.append(x_axis_pattern)
                else:
                    if j == 0 or j == max(range(x_axis)):
                        x_axis_values.append(y_axis_pattern)
                    else:
                        x_axis_values.append(" ")
            plot.append(x_axis_values)
        
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
