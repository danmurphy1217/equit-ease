from __future__ import annotations
import dataclasses
from typing import Any, List

from equit_ease.parser.parse import Parser
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


class HistoricalDisplayer(Displayer):
    """"contains methods used solely for the displayment of the chart data."""



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

                formatted_key = self.set_formatting(key, ["split", "capitalize"])
                max_padding = (
                    len(formatted_key)
                    if len(formatted_key) > len(str(value))
                    else len(str(value))
                )
                row_one.append(formatted_key), row_two.append(value)
                padding_sizes.append(max_padding)

        def aggregate(*args):
            result = []
            for arg in args:
                for separator in arg:
                    result.append(separator)
            return result

        return aggregate(
            self._build_table(padding_sizes, rows=[row_one]),
            self._build_table(padding_sizes, rows=[row_two]),
        )

    def _build_table(self: QuoteDisplayer, padding_size: List[int], **kwargs):
        def build_column_separators(row: List[str], padding_sizes: List[str]) -> str:
            """
            build the separators that exist between each column.

            :param row -> ``List[str]``: the row to format with separators and spacing.
            :param padding_sizes -> ``List[str]``: the sizes of padding to assign to each value.
                                                   Must be in the same order as the values they should be assigned to.
            :returns result -> ``str``: the formatted row with '|' separators between each column.

            :example:

                    >>> row = [160.8, 160.81, 169.66, 170.0, '159.44 - 178.6199', 12440181, 101560188928, 'N/A']
                    >>> padding_sizes = [5, 6, 6, 5, 17, 8, 12, 3]
                    >>> build_column_separators(row, padding_sizes)

                        | 160.8 | 160.81 | 169.66 | 170.0 | 159.44 - 178.6199 | 12440181 | 101560188928 | N/A |
            """
            result = " | "
            for i, item in enumerate(row):
                stringified_item = str(item)
                padding = padding_sizes[i]
                leading_whitespace = " " * (padding - len(str(item)))
                result += leading_whitespace + stringified_item + " | "

            return result

        def build_row_separators(row: List[str]) -> str:
            """
            build the separators that exist between each row.

            :param row -> ``List[str]``: the row used to determine the length of the separator.
            :returns result -> ``str``: a string len(row) long used as the separator.

            :example:
                1.
                    >>> build_row_sepaarators(5)
                    -----
                2.
                    >>> build_row_sepaarators(10)
                    ----------
            """
            result = "-" * (len(row))
            return result

        rows = kwargs["rows"]

        for row in rows:
            formatted_row = build_column_separators(row, padding_size)
            formatted_col = build_row_separators(formatted_row)
            return formatted_col, formatted_row

    def __repr__(self, key: str, value: Any) -> str:
        """
        builds a string representation of a key-value pair of EquityMeta.

        :param key -> ``str``: a key from an EquityMeta object.
        :param value -> ``str``: a value associated with ``key``.

        :returns result -> ``str``: a string representation of the key-value pair.

        :example:
            1.
                >>> __repr__('hello_world', 'hi!')
                    Hello World: *hi!* # the key is split at '_' and capitalized, the value is underlined and bolded (color not shown).
                                 ---
        """
        formatted_key = self.set_formatting(key, ["split", "capitalize", "bold"])
        formatted_value = self.set_formatting(value, ["color", "bold", "underline"])
        result = self.set_formatting(f"{formatted_key}: {formatted_value}\n", "align")
        return result
