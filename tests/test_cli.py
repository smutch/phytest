from pathlib import Path

import pytest
from typer.testing import CliRunner

from phytest.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "TESTFILE  Path to test file.  [required]" in result.stdout


def test_cli_no_input_file(request: pytest.FixtureRequest):
    result = runner.invoke(app, [str(request.path.parent / "input/testfile1.py")])
    assert result.exit_code == 0
    assert "testfile1.py" in result.stdout
    assert "1 passed" in result.stdout


def test_cli_basic(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
        ],
    )
    assert "7 passed" in result.stdout


def test_cli_basic_expression(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
            "-k",
            "test_tree_number_of_tips",
        ],
    )
    assert "1 passed" in result.stdout
    assert "6 deselected" in result.stdout


def test_cli_report(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
            "-r",
            "pytest-report.html",
        ],
    )
    assert Path("pytest-report.html").exists()


def test_cli_report_invalid(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
            "-r",
            "pytest-report.txt",
        ],
    )
    assert isinstance(result.exception, ValueError)
    assert str(result.exception) == "Report must use .html extension."


def test_cli_missing_sequence_file(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
            "-v",
        ],
    )
    assert "ValueError: test_length requires a sequence file" in result.stdout


def test_cli_invalid_tree_format(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-t",
            "examples/data/example.tree",
            "-s",
            "examples/data/example.fasta",
            "-d",
            "examples/data/example.csv",
            "--tree-format",
            "excel",
            "-v",
        ],
    )
    assert (
        "Error: Invalid value for '--tree-format': 'excel' is not a valid tree format. Must be one of newick, nexus, phyloxml, nexml."
        in result.stdout
    )


def test_cli_invalid_data_format(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-t",
            "examples/data/example.tree",
            "-s",
            "examples/data/example.fasta",
            "-d",
            "examples/data/example.csv",
            "--data-format",
            "pdf",
            "-v",
        ],
    )
    assert (
        "Error: Invalid value for '--data-format': 'pdf' is not a valid data format. Must be one of csv, tsv, excel"
        in result.stdout
    )


def test_cli_invalid_sequence_format(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-t",
            "examples/data/example.tree",
            "-s",
            "examples/data/example.fasta",
            "-d",
            "examples/data/example.csv",
            "--sequence-format",
            "pdf",
            "-v",
        ],
    )
    assert "Error: Invalid value for '--sequence-format': 'pdf' is not" in result.stdout


def test_cli_invalid_data(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-t",
            "phytest/bio/tree.py",  # should not be read
            "-d",
            "phytest/bio/data.py",
            "-v",
        ],
    )
    assert "ValueError: test_length requires a sequence file" in result.stdout


def test_cli_missing_tree_file(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-d",
            "examples/data/example.csv",
            "-v",
        ],
    )
    assert "ValueError: test_tree_number_of_tips requires a tree file" in result.stdout


def test_cli_missing_data_file(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/basic.py"),
            "-s",
            "examples/data/example.fasta",
            "-t",
            "examples/data/example.tree",
            "-v",
        ],
    )
    assert "ValueError: test_data_number_of_rows requires a data file" in result.stdout


def test_cli_missing_alignment_file(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/alignment.py"),
            "-t",
            "examples/data/example.tree",
            "-d",
            "examples/data/example.csv",
            "-v",
        ],
    )
    assert "ValueError: test_alignment_length requires an alignment file" in result.stdout


def test_cli_alignment(request: pytest.FixtureRequest):
    result = runner.invoke(
        app,
        [
            str(request.path.parent / "input/alignment.py"),
            "-s",
            "examples/data/example.fasta",
            "-v",
        ],
    )
    assert "1 passed" in result.stdout
