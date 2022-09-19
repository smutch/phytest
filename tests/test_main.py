from unittest.mock import patch

import pytest

from phytest import main


def test_main_basic(request: pytest.FixtureRequest):
    result = main(
        str(request.path.parent / "input/basic.py"),
        sequence="examples/data/example.fasta",
        tree="examples/data/example.tree",
        data="examples/data/example.csv",
    )
    assert result.value == 0


def test_tree_not_found(request: pytest.FixtureRequest, capsys):
    result = main(
        str(request.path.parent / "input/basic.py"),
        sequence="examples/data/example.fasta",
        tree="examples/data/NOTFOUND.tree",
        data="examples/data/example.csv",
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: Unable to locate requested t" in captured.out
    assert result.value != 0


def test_data_not_found(request: pytest.FixtureRequest, capsys):
    result = main(
        str(request.path.parent / "input/basic.py"),
        sequence="examples/data/example.fasta",
        tree="examples/data/example.tree",
        data="examples/data/NOTFOUND.csv",
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: Unable to locate requested d" in captured.out
    assert result.value != 0


def test_sequence_not_found(request: pytest.FixtureRequest, capsys):
    result = main(
        str(request.path.parent / "input/basic.py"),
        sequence="examples/data/NOTFOUND.fasta",
        tree="examples/data/example.tree",
        data="examples/data/example.csv",
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: Unable to locate requested s" in captured.out
    assert result.value != 0


def test_alignment_not_found(capsys):
    result = main(
        "examples/example.py",
        sequence="examples/data/NOTFOUND.fasta",
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: Unable to locate requested al" in captured.out
    assert result.value != 0


@patch.object(pytest, 'main')
def test_auto_testfile(pytest_main):
    main()
    pytest_main.assert_called_once()
    assert pytest_main.mock_calls[0].args[0][0].name == "test_main.py"
