from pathlib import Path
from typing import Optional

from Bio.AlignIO import _FormatToIterator as supported_alignment_formats
from Bio.Phylo._io import supported_formats as supported_tree_formats
from Bio.SeqIO import _FormatToIterator as supported_sequence_formats

supported_sequence_formats.update(supported_alignment_formats)
import typer

from .main import main

app = typer.Typer()


def sequence_format_callback(value: str):
    if value not in supported_sequence_formats:
        raise typer.BadParameter(
            f"'{value}' is not a valid sequence format. Must be one of {', '.join(supported_sequence_formats.keys())}."
        )
    return value


def tree_format_callback(value: str):
    if value not in supported_tree_formats:
        raise typer.BadParameter(
            f"'{value}' is not a valid tree format. Must be one of {', '.join(supported_tree_formats.keys())}."
        )
    return value


def data_format_callback(value: str):
    if value not in ['csv', 'tsv', 'excel']:
        raise typer.BadParameter(f"'{value}' is not a valid data format. Must be one of csv, tsv, excel.")
    return value


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def cli(
    testfile: Path = typer.Argument(..., help="Path to test file."),
    sequence: Optional[Path] = typer.Option(
        None, "--sequence", "-s", dir_okay=False, exists=True, help="Path to sequence file."
    ),
    sequence_format: Optional[str] = typer.Option(
        'fasta',
        "--sequence-format",
        dir_okay=False,
        exists=True,
        help=f"{', '.join(supported_sequence_formats.keys())}.",
        callback=sequence_format_callback,
    ),
    tree: Optional[Path] = typer.Option(None, "--tree", "-t", dir_okay=False, exists=True, help="Path to tree file."),
    tree_format: Optional[str] = typer.Option(
        'newick',
        "--tree-format",
        dir_okay=False,
        exists=True,
        help=f"{', '.join(supported_tree_formats.keys())}.",
        callback=tree_format_callback,
    ),
    data: Optional[Path] = typer.Option(None, "--data", "-d", dir_okay=False, exists=True, help="Path to data file."),
    data_format: Optional[str] = typer.Option(
        'csv', "--data-format", dir_okay=False, exists=True, help="csv, tsv, excel.", callback=data_format_callback
    ),
    report: Optional[Path] = typer.Option(
        None, "--report", "-r", dir_okay=False, exists=False, help="Path to HTML report to generate."
    ),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    expression: Optional[str] = typer.Option(
        None, "-k", help="Only run tests which match the given substring expression."
    ),
    cores: Optional[str] = typer.Option(
        None,
        "-n",
        help="Number of cores. Use 'auto' to spawn a number of workers processes equal to the number of available CPUs.",
    ),
):
    exit_code = main(
        testfile=testfile,
        sequence=sequence,
        sequence_format=sequence_format,
        tree=tree,
        tree_format=tree_format,
        data=data,
        data_format=data_format,
        verbose=verbose,
        report=report,
        expression=expression,
        cores=cores,
    )
    raise typer.Exit(code=exit_code)
