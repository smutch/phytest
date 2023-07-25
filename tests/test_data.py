import re

import pytest

from phytest import Data
from phytest.utils import PhytestAssertion, PhytestWarning


def test_data_read():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data_path = 'examples/data/example.tsv'
    data = Data.read(data_path, 'tsv')
    data_path = 'examples/data/example.xlsx'
    data = Data.read(data_path, 'excel')


def test_data_read_invalid():
    data_path = 'examples/data/example.csv'
    with pytest.raises(ValueError, match="Data format must be one of csv, tsv, excel"):
        Data.read(data_path, 'txt')


def test_assert_data_contains():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data.assert_contains('name', 'Sequence_A')
    with pytest.raises(
        PhytestAssertion,
        match=re.escape(
            "The values of column 'name' are '['Sequence_A' 'Sequence_B' 'Sequence_C' 'Sequence_D']'.\nThe column 'name' does not contain 'Sequence_X'."
        ),
    ):
        data.assert_contains('name', 'Sequence_X')


def test_assert_data_match():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data.assert_match('name', 'Sequence_.')
    with pytest.raises(
        PhytestAssertion,
        match=re.escape(
            "The values of column 'name' are '['Sequence_A' 'Sequence_B' 'Sequence_C' 'Sequence_D']'.\nThe row(s) '[3]' of the column 'name' do not match the pattern 'Sequence_[A-C]'."
        ),
    ):
        data.assert_match('name', 'Sequence_[A-C]')


def test_assert_data_allowed_columns():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data.assert_columns(['name', 'date', 'sequence'])
    with pytest.raises(
        PhytestAssertion,
        match=re.escape("The columns '['date']' are not in the list of allowed columns '['name', 'sequence']'."),
    ):
        data.assert_columns(['name', 'sequence'])
    with pytest.raises(
        PhytestAssertion,
        match=re.escape("The column names do not exactly match the list of allowed columns"),
    ):
        data.assert_columns(['name', 'date', 'sequence'], exact=True)


def test_assert_data_allowed_values():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data.assert_values('name', ['Sequence_A', 'Sequence_B', 'Sequence_C', 'Sequence_D', 'Sequence_E'])
    with pytest.raises(
        PhytestAssertion,
        match=re.escape(
            "The row(s) '[3]' of the column 'name' are not in the list of allowed values '['Sequence_A', 'Sequence_B', 'Sequence_C']"
        ),
    ):
        data.assert_values('name', ['Sequence_A', 'Sequence_B', 'Sequence_C'])

    # exact
    with pytest.raises(
        PhytestAssertion,
        match=re.escape("The values column 'name' do not exactly match the allowed values"),
    ):
        data.assert_values('name', ['Sequence_A', 'Sequence_B', 'Sequence_C', 'Sequence_D', 'Sequence_E'], exact=True)

    # allow nan
    data.replace('Sequence_D', float('nan'), inplace=True)
    data.assert_values('name', ['Sequence_A', 'Sequence_B', 'Sequence_C'], allow_nan=True)
    with pytest.raises(
        PhytestAssertion,
        match=re.escape(
            "The row(s) '[3]' of the column 'name' are not in the list of allowed values '['Sequence_A', 'Sequence_B', 'Sequence_C']'."
        ),
    ):
        data.assert_values('name', ['Sequence_A', 'Sequence_B', 'Sequence_C'])


def test_assert_range():
    data_path = 'examples/data/example.csv'
    data = Data.read(data_path, 'csv')
    data['value'] = [1, 2, 3, 4]
    data.assert_range('value', min=1, max=5)
    with pytest.raises(
        PhytestAssertion,
        match=re.escape("The maximum value of column 'value' is '4', which is greater than '3'."),
    ):
        data.assert_range('value', max=3)
    with pytest.raises(
        PhytestAssertion,
        match=re.escape("The minimum value of column 'value' is '1', which is less than '2'."),
    ):
        data.assert_range('value', min=2)
