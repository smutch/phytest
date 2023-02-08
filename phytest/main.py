import inspect
import os
from pathlib import Path
from typing import Optional

import pytest


def main(
    testfile: Optional[Path] = None,
    sequence: Optional[Path] = None,
    sequence_format: Optional[str] = 'fasta',
    tree: Optional[Path] = None,
    tree_format: Optional[str] = 'newick',
    data: Optional[Path] = None,
    data_format: Optional[str] = 'csv',
    verbose: bool = False,
    report: Optional[Path] = None,
    expression: Optional[str] = None,
    cores: Optional[str] = None,
):
    if not testfile:
        testfile = Path(os.path.abspath((inspect.stack()[1])[1]))
    args = [testfile]
    if not verbose:
        args.extend(["-ra", "--tb=no", "--no-header"])
    else:
        args.extend(["-v"])
    if sequence is not None:
        args.extend(["--sequence", sequence])
        args.extend(["--sequence-format", sequence_format])
    if tree is not None:
        args.extend(["--tree", tree])
        args.extend(["--tree-format", tree_format])
    if data is not None:
        args.extend(["--data", data])
        args.extend(["--data-format", data_format])
    if report:
        if not str(report).endswith('.html'):
            raise ValueError(f"Report must use .html extension.")
        args.extend([f"--html={report}", "--self-contained-html", f"--css={Path(__file__).parent / 'report/logo.css'}"])
    if expression:
        # only run tests which match the given substring expression
        # see the pytest help
        args.extend(["-k", expression])
    if cores:
        # parallel with pytest-xdist
        args.extend(["-n", cores])
    exit_code = pytest.main(args, plugins=['phytest'])
    return exit_code
