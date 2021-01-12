from __future__ import annotations
from datetime import datetime
import os
import dataclasses
from typing import Any, List, Tuple, Set
import random

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

    def _set_axes(self):
        """builds the axes and core plot for the chart."""

        plot = []
        n_columns = (3 * os.get_terminal_size().columns) // 4
        n_rows = (os.get_terminal_size().lines) // 2

        x_axis_indices = self._build_five_num_summary(n_columns)
        x_axis_labels = self._build_x_axis_labels(n_columns, *x_axis_indices)
        y_axis_indices = self._build_five_num_summary(n_rows)
        y_axis_labels = self._build_y_axis_labels(n_rows, *y_axis_indices)[::-1]

        max_width = len(max(y_axis_labels, key=len))
        padded_y_axis_labels = self._set_padding(y_axis_labels, max_width)
        padded_x_axis_labels = max_width * " " + x_axis_labels

        plot = self._build_plot(len(x_axis_labels), n_rows, "-", "|")

        # TODO: get tuple containing (TIME, PRICE) info for the y_axis_labels
        only_numbers = filter(
            lambda val: int(val.strip()) if val.strip() != "" else None, x_axis_labels
        )

        for i, price_label in enumerate(y_axis_labels):
            stripped_price = price_label.strip()
            clean_price = (
                float(stripped_price) if stripped_price != "" else stripped_price
            )
            if clean_price != "":
                price_index = self.y_axes.index(clean_price)
                time = self.x_axes[price_index]
                if datetime.fromtimestamp(time).strftime("%H") in x_axis_labels:
                    plot[i][
                        x_axis_labels.index(datetime.fromtimestamp(time).strftime("%H"))
                    ] = Formatter.bold(Formatter.set_color_for("0"))
                    print(
                        clean_price,
                        i,
                        price_index,
                        x_axis_labels.index(
                            datetime.fromtimestamp(time).strftime("%H")
                        ),
                    )

        plot.append(padded_x_axis_labels)
        for i, line in enumerate(plot):
            if isinstance(line, list):
                # line[random.choice(x_axis_indices)] = Formatter.set_color_for('O')
                line.insert(0, padded_y_axis_labels[i])

            print("".join(line))

    def _build_x_axis_labels(self, n_columns: int, *args: str) -> str:
        """
        build x axis labels for the plot.

        :param n_columns -> ``int``: the number of columns in the plot.
        :args -> ``str``: should contain the indices on which the labels should be placed.

        :returns result -> ``str``: a formatted list of x-axis labels
        """
        labels = [" "] * n_columns
        five_num_summary = self._build_five_num_summary(self.x_axes)

        for i, arg in enumerate(args):
            labels[arg] = datetime.fromtimestamp(five_num_summary[i]).strftime("%H")

        return "".join(labels)

    def _build_y_axis_labels(self, n_rows: int, *args: str) -> str:
        """
        build y axis labels for the plot.

        :param n_rows: -> the number of rows in the plot.
        :args -> ``str``: should contain the indices on which the labels should be placed.
        """
        labels = [" "] * n_rows
        five_num_summary = self._build_five_num_summary(sorted(self.y_axes))

        for i, arg in enumerate(args):
            labels[arg] = str(five_num_summary[i])

        return labels

    def _set_padding(self, labels: List[str], max_width: int):
        """
        adds whitespace along the y-axis to align labels.

        :param labels -> ``List[str]``: the labels for the y axis of the plot.

        :returns result -> ``List[str]``:  padded y axis labels.
        """
        padded_labels = []

        for label in labels:
            label_length_diff = max_width - len(label)
            padding = " " * label_length_diff
            padded_label = padding + label + " "
            padded_labels.append(padded_label)

        return padded_labels

    def _build_plot(
        self, x_axis: int, y_axis: int, x_axis_pattern: str, y_axis_pattern: str
    ) -> List[List[str]]:
        """
        build plot used to display price and/or volume data.

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
                if i == 0 or i == max(range(y_axis)):
                    x_axis_values.append(x_axis_pattern)
                else:
                    if j == 0 or j == max(range(x_axis)):
                        x_axis_values.append(y_axis_pattern)
                    else:
                        x_axis_values.append(" ")
            plot.append(x_axis_values)

        return plot

    def _build_five_num_summary(self, data: List or Tuple or Set):
        """
        creates a five number summart for the provided `data`

        :param data -> ``List`` | ``Tuple`` | ``Set``: the data to create a five-number summary for.

        :returns result -> ``Tuple``: five-number summary from min -> max.
        """
        range_for_data = range(data) if isinstance(data, int) else data

        def get_min() -> int:
            """retrieve the minimum from the data."""
            return range_for_data[0]

        def get_max() -> int:
            """retrieve the maximum from the data."""
            return range_for_data[-1]

        def get_quartile(quartile: int) -> int:
            """retrieve a valid quartile. If not valid, a ValueError is thrown."""
            if quartile not in (1, 2, 3):
                raise ValueError(
                    "quartile must be one of the following values: 1, 2, 3."
                )
            else:
                if quartile == 1:
                    return range_for_data[len(range_for_data) // 4]
                elif quartile == 2:
                    return range_for_data[len(range_for_data) // 2]
                else:
                    return range_for_data[(3 * len(range_for_data)) // 4]

        return (get_min(), get_quartile(1), get_quartile(2), get_quartile(3), get_max())

    def plot(self, *args, **kwargs):
        """"""
        # TODO


class QuoteDisplayer(Displayer):
    """contains methods used solely for the displayment of quote data."""

    def stringify(self: QuoteDisplayer) -> str:
        """
        str representation of the quote meta-data.

        :param self -> ``QuoteDisplayer``:
        """
        dataclass_as_dict = dataclasses.asdict(self.data)

        s = """\n"""
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
        formatted_key = " ".join(self.set_formatting(key, "bold").split("_"))
        formatted_value = self.set_formatting(value, ["color", "bold", "underline"])
        result = self.set_formatting(f"{formatted_key}: {formatted_value}\n", "align")
        return result
