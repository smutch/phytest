==============
Writing Tests
==============

Phytest is easily extendable and provides a simple interface for writing custom phylogenetic tests.
The interface follows the Pytest model of testing i.e. tests are defined as Python functions (or class methods)
containing assert statements that are collected and evaluated at run-time. Tests that fail are captured and reported
to the user allowing for repeatable and automated testing.
Phytest provides many convenient helper functions for testing phylogenetic analyses including methods for testing sequences,
alignments, trees and metadata files.

Phytest fixtures
=================

Phytest injects special fixture objects into test functions, allowing for easy evaluation and
testing of phylogenetic data structures. These fixtures provide the standard Biopython (sequences and trees) and Pandas (metadata)
class methods as well as special assert methods for testing these data structures.

Only functions that require the fixtures will have the Pytest objects passed to them. For example consider the following tests.

.. code-block:: python

    from phytest import Sequence

    def test_example(sequence: Sequence):
        ...

Test functions must start with the keyword :code:`test_` this allows Pytest to identify and collect the tests.
Fixtures are required using one of the special arguments i.e. the lower case of the class name.

Here the :code:`sequence` argument is used to require the sequences passed from the command line
(see below for information on how to pass files to Phytest). Phytest will identify which test functions
require which fixtures and pass the Phytest objects to them for testing.

Using Phytest classes for type hints is not required, however, makes for a better development experience.
For example the following is a valid Phytest test and will be passed a Sequence object.

.. code-block:: python

    def test_example(sequence):
        ...

Fixtures can be combined to make more complex tests across multiple data types e.g.

.. code-block:: python

    from phytest import Sequence, Tree

    def test_example(sequence: Sequence, tree: Tree):
        # test tree and sequence objects together
        ...

Sequence
---------

The Phytest Sequence class is a sub-class of the Biopython SeqRecord class. This class uses the fixture :code:`sequence`.

.. code-block:: python

    from phytest import Sequence

    def test_example(sequence: Sequence):
        ...

Any tests requiring the class will be run for every sequence in the file. For example if the fasta file below is passed to Phytest
the :code:`test_example` function above would be run 4 times (Sequence_A-Sequence_D).

.. code-block:: text

    >Sequence_A
    ATGAGATCCCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_B
    ATGAGATCCCCGATAGCGAGCTAGXGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_C
    ATGAGA--CCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_D
    ATGAGATCCCCGATAGCGAGCTAGCGATNNNNNNNNNNNNNNNNNTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG

.. code-block:: bash

    $ phytest test.py --sequence sequences.fasta

    Test session starts (platform: darwin, Python 3.9.12, pytest 7.1.1, pytest-sugar 0.9.4)
    rootdir: /Users/wytamma/programming/phytest, configfile: pyproject.toml
    plugins: sugar-0.9.4, html-3.1.1, cov-3.0.0
    collecting ...
    test.py ✓✓✓✓                                                            100% ██████████

    Results (0.03s):
        4 passed


Alternative file formats can be specified using the :code:`--sequence-format` flag.

Alignment
---------

The Phytest Alignment class is a sub-class of the Biopython MultipleSeqAlignment class. This class uses the fixture :code:`alignment`.

.. code-block:: python

    from phytest import Alignment

    def test_example(alignment: Alignment):
        ...

Tests using the alignment file will be run once i.e. you will have access to the entire alignment during the test.
Alignments are also passed to Phytest using the :code:`--sequence` flag however they are required to be valid
alignments e.g. all sequence must be the same length.

.. code-block:: bash

    phytest test.py --sequence sequences.fasta

    Test session starts (platform: darwin, Python 3.9.12, pytest 7.1.1, pytest-sugar 0.9.4)
    rootdir: /Users/wytamma/programming/phytest, configfile: pyproject.toml
    plugins: sugar-0.9.4, html-3.1.1, cov-3.0.0
    collecting ...
    test.py ✓                                                               100% ██████████

    Results (0.02s):
        1 passed


Alternative file formats can be specified using the :code:`--sequence-format` flag.

Tree
-----

The Phytest Tree class is a sub-class of the Biopython Tree class. This class uses the fixture :code:`tree`.

.. code-block:: python

    from phytest import Tree

    def test_example(tree: Tree):
        ...

Tests using the tree fixture will be run once per tree in the file. Tree files are passed to Phytest using the :code:`--tree` flag.

.. code-block:: text

    (Sequence_A:1,Sequence_B:0.2,(Sequence_C:0.3,Sequence_D:0.4):0.5);
    (Sequence_A:1,Sequence_B:0.3,(Sequence_C:0.3,Sequence_D:0.4):0.5);


.. code-block:: bash

    phytest test.py --tree tree.newick

    Test session starts (platform: darwin, Python 3.9.12, pytest 7.1.1, pytest-sugar 0.9.4)
    rootdir: /Users/wytamma/programming/phytest, configfile: pyproject.toml
    plugins: sugar-0.9.4, html-3.1.1, cov-3.0.0
    collecting ...
    test.py ✓✓                                                              100% ██████████

    Results (0.02s):
        2 passed

Alternative file formats can be specified using the :code:`--tree-format` flag.

Data
-----

The Phytest Data class is a sub-class of the Pandas DataFrame class. This class uses the fixture :code:`data`.

.. code-block:: python

    from phytest import Data

    def test_example(data: Data):
        ...

Tests using the data file will be run once. Data files are passed to Phytest using the :code:`--data` flag.

.. code-block:: bash

    phytest test.py --data metadata.csv

    Test session starts (platform: darwin, Python 3.9.12, pytest 7.1.1, pytest-sugar 0.9.4)
    rootdir: /Users/wytamma/programming/phytest, configfile: pyproject.toml
    plugins: sugar-0.9.4, html-3.1.1, cov-3.0.0
    collecting ...
    test.py ✓                                                               100% ██████████

    Results (0.02s):
        1 passed


Alternative file formats can be specified using the :code:`--data-format` flag.


Built-in asserts
=================

Phytest provides many convenient helper functions for testing phylogenetic analyses including methods for testing sequences,
alignments, trees and metadata files.

.. code-block:: python

    from phytest import Sequence

    def test_GC_content(sequence: Sequence):
        sequence.assert_percent_GC(38)

For example, the Phytest Sequence class implements the method :code:`Sequence.assert_percent_GC`.
Calling this method with the expected GC-content e.g. :code:`sequence.assert_percent_GC(38)` will
raise an error if the percent of G and C nucleotides in the sequence is not equal to 38%.
Many methods also provide maximum and minimum arguments so the upper and lower bounds can be tested
e.g. :code:`sequence.assert_percent_GC(min=30, max=40)`.

.. code-block:: python

    from phytest import Sequence

    def test_GC_content(sequence: Sequence):
        sequence.assert_percent_GC(min=30, max=40)

All Phytest assert methods also provide a warning flag e.g. :code:`sequence.assert_percent_GC(38, warn=True)`
causing the method to raise a warning instead of an error if the test fails. In an automated pipeline,
this provides a way to inform the user of potential problems without causing the pipeline to fail.
The warning flag can be set automatically by calling the method with the :code:`warn_` prefix instead
of :code:`assert_` e.g. :code:`sequence.warn_percent_GC(38)`.

.. code-block:: python

    from phytest import Sequence

    def test_GC_content(sequence: Sequence):
        sequence.warn_percent_GC(38)

See the documentation for a full list of built-in assert methods (https://phytest-devs.github.io/phytest/reference.html).


Custom asserts
=================

As Phytest is running Pytest under the hood it is trivial to write your own custom asserts using the Phytest fixtures.

.. code-block:: python

    def test_outlier_branches(tree: Tree):
        # Here we create a custom function to detect outliers
        import statistics

        tips = tree.get_terminals()
        branch_lengths = [t.branch_length for t in tips]
        cut_off = statistics.mean(branch_lengths) + statistics.stdev(branch_lengths)
        for tip in tips:
            assert tip.branch_length < cut_off, f"Outlier tip '{tip.name}' (branch length = {tip.branch_length})!"
