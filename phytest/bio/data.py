import re
from typing import List, Union

import pandas as pd
from pandas import DataFrame

from ..utils import PhytestObject, assert_or_warn


class Data(PhytestObject, DataFrame):
    @classmethod
    def read(cls, data_path, data_format) -> 'Data':
        allowed_formats = ['csv', 'tsv', 'excel']
        if data_format not in allowed_formats:
            raise ValueError(f'Data format must be one of {", ".join(allowed_formats)}.')
        if data_format == 'csv':
            df = pd.read_csv(data_path)
        elif data_format == 'tsv':
            df = pd.read_csv(data_path, sep='\t')
        elif data_format == 'excel':
            df = pd.read_excel(data_path, engine='openpyxl')
        return Data(df)

    def assert_contains(
        self,
        column: str,
        value: str,
        *,
        warning: bool = False,
    ) -> None:
        """
        Asserts that specified column contains the specified value.

        Args:
            column (str, required): The column to check.
            value (str, required): the value to look for.
            warning (bool): If True, raise a warning instead of an exception. Defaults to False.
                This flag can be set by running this method with the prefix `warn_` instead of `assert_`.
        """
        column_values = self[column].values
        summary = f"The values of column '{column}' are '{column_values}'."
        assert_or_warn(
            value in column_values,
            warning,
            summary,
            f"The column '{column}' does not contain '{value}'.",
        )

    def assert_match(
        self,
        column: str,
        pattern: str,
        *,
        warning: bool = False,
    ) -> None:
        """
        Asserts that all values of the specified column match the specified pattern.

        Args:
            column (str, required): The column to check.
            pattern (str, required): The pattern to match.
            warning (bool): If True, raise a warning instead of an exception. Defaults to False.
                This flag can be set by running this method with the prefix `warn_` instead of `assert_`.
        """
        column_values = self[column].values
        summary = f"The values of column '{column}' are '{column_values}'."
        not_matched = self[~self[column].str.contains(re.compile(pattern))].index.values
        assert_or_warn(
            len(not_matched) == 0,
            warning,
            summary,
            f"The row(s) '{not_matched}' of the column '{column}' do not match the pattern '{pattern}'.",
        )

    def assert_columns(
        self,
        allowed_columns: List[str],
        *,
        exact: bool = False,
        warning: bool = False,
    ) -> None:
        """
        Asserts that the specified column(s) are in the DataFrame.

        Args:
            allowed_columns (List[str], required): The list of allowed columns.
            exact (bool): If True, the list of allowed columns must be exactly the same as the list of columns in the DataFrame.
            warning (bool): If True, raise a warning instead of an exception. Defaults to False.
                This flag can be set by running this method with the prefix `warn_` instead of `assert_`.
        """
        columns = self.columns.values
        summary = f"The names of the columns are '{columns}'."
        if exact:
            not_allowed = list(set(allowed_columns).symmetric_difference(set(columns)))
            message = f"The column names do not exactly match the list of allowed columns '{allowed_columns}'."
        else:
            not_allowed = [column for column in columns if column not in allowed_columns]
            message = f"The columns '{not_allowed}' are not in the list of allowed columns '{allowed_columns}'."
        assert_or_warn(len(not_allowed) == 0, warning, summary, message)

    def assert_values(
        self,
        column: str,
        values: list,
        *,
        allow_nan: bool = False,
        exact: bool = False,
        warning: bool = False,
    ) -> None:
        """
        Asserts that all values of the specified column are in the specified list of allowed values.

        Args:
            column (str, required): The column to check.
            values (list, required): The list of allowed values.
            allow_nan (bool): If True, allow NaN values.
            exact (bool): If True, the list of allowed values must be exactly the same as the list of values in the DataFrame.
            warning (bool): If True, raise a warning instead of an exception. Defaults to False.
                This flag can be set by running this method with the prefix `warn_` instead of `assert_`.
        """

        column_values = self[column].values
        summary = f"The values of column '{column}' are '{column_values}'."
        if allow_nan:
            values.append(float('nan'))
        if exact:
            not_allowed = list(set(values).symmetric_difference(set(column_values)))
            message = f"The values column '{column}' do not exactly match the allowed values '{values}'"
        else:
            not_allowed = self[~self[column].isin(values)].index.values
            message = (
                f"The row(s) '{not_allowed}' of the column '{column}' are not in the list of allowed values '{values}'."
            )
        assert_or_warn(len(not_allowed) == 0, warning, summary, message)

    def assert_range(
        self,
        column: str,
        *,
        min: Union[int, float] = None,
        max: Union[int, float] = None,
        warning: bool = False,
    ) -> None:
        """
        Asserts that all values of the specified column are in the specified range.

        Args:
            column (str, required): The column to check.
            min (Union[int, float]): The minimum value of the range.
            max (Union[int, float]): The maximum value of the range.
            warning (bool): If True, raise a warning instead of an exception. Defaults to False.
                This flag can be set by running this method with the prefix `warn_` instead of `assert_`.
        """
        column_values = self[column].values
        summary = f"The values of column '{column}' are '{column_values}'."
        if min is not None:
            assert_or_warn(
                min <= column_values.min(),
                warning,
                summary,
                f"The minimum value of column '{column}' is '{column_values.min()}', which is less than '{min}'.",
            )
        if max is not None:
            assert_or_warn(
                max >= column_values.max(),
                warning,
                summary,
                f"The maximum value of column '{column}' is '{column_values.max()}', which is greater than '{max}'.",
            )
