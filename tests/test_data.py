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
