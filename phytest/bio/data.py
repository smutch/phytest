import re

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
