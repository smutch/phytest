.. image:: https://raw.githubusercontent.com/phytest-devs/phytest/main/docs/images/logo.png
  :alt: Phytest logo

.. start-badges

|pypi badge| |tests badge| |coverage badge| |docs badge| |black badge| |pre-commit badge| |doi badge|


.. |pypi badge| image:: https://img.shields.io/pypi/v/phytest.svg
    :target: https://pypi.org/project/phytest/

.. |tests badge| image:: https://github.com/phytest-devs/phytest/workflows/tests/badge.svg
    :target: https://github.com/phytest-devs/phytest/actions

.. |docs badge| image:: https://github.com/phytest-devs/phytest/workflows/docs/badge.svg
    :target: https://phytest-devs.github.io/phytest/

.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/smutch/e8160655e03d9015b1e93b97ed611f4f/raw/coverage-badge.json
    :target: https://phytest-devs.github.io/phytest/coverage/

.. |pre-commit badge| image:: https://results.pre-commit.ci/badge/github/phytest-devs/phytest/main.svg
    :target: https://results.pre-commit.ci/latest/github/phytest-devs/phytest/main

.. |doi badge| image:: https://img.shields.io/badge/DOI-10.21203%2Frs.3.rs1903486%2Fv1-success.svg
    :target: https://www.researchsquare.com/article/rs-1903486/v1

.. end-badges



Phytest: Quality Control for Phylogenetic Analyses.

----

Documentation: https://phytest-devs.github.io/phytest

Code: https://github.com/phytest-devs/phytest

Tutorials: https://github.com/phytest-devs?q=example

----

.. start-quickstart

Installation
============
Install phytest using pip:

.. code-block:: bash

    pip install phytest


Quick Start
============

Phytest is a tool for automating quality control checks on sequence, tree and metadata files during phylogenetic analyses.
Phytest ensures that phylogenetic analyses meet user-defined quality control tests.

Here we will create example data files to run our tests on.

Create an alignment fasta file :code:`example.fasta`

.. code-block:: text

    >Sequence_A
    ATGAGATCCCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_B
    ATGAGATCCCCGATAGCGAGCTAGXGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_C
    ATGAGA--CCCGATAGCGAGCTAGCGATCGCAGCGACTCAGCAGCTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG
    >Sequence_D
    ATGAGATCCCCGATAGCGAGCTAGCGATNNNNNNNNNNNNNNNNNTACAGCGCAGAGGAGAGAGAGGCCCCTATTTACTAGAGCTCCAGATATAGNNTAG

Create a tree newick file :code:`example.tree`

.. code-block:: text

    (Sequence_A:1,Sequence_B:0.2,(Sequence_C:0.3,Sequence_D:0.4):0.5);

Writing a test file
########################

We want to enforce the follow constraints on our data:
    1. The alignment has 4 sequences
    2. The sequences have a length of 100
    3. The sequences only contains the characters A, T, G, C, N and -
    4. The sequences are allowed to only contain single base deletions
    5. The longest stretch of Ns is 10
    6. The tree has 4 tips
    7. The tree is bifurcating
    8. There are no outlier branches in the tree

We can write these tests in a python files :code:`example.py`

.. code-block:: python

    from phytest import Alignment, Sequence, Tree


    def test_alignment_has_4_sequences(alignment: Alignment):
        alignment.assert_length(4)


    def test_alignment_has_a_width_of_100(alignment: Alignment):
        alignment.assert_width(100)


    def test_sequences_only_contains_the_characters(sequence: Sequence):
        sequence.assert_valid_alphabet(alphabet="ATGCN-")


    def test_single_base_deletions(sequence: Sequence):
        sequence.assert_longest_stretch_gaps(max=1)


    def test_longest_stretch_of_Ns_is_10(sequence: Sequence):
        sequence.assert_longest_stretch_Ns(max=10)


    def test_tree_has_4_tips(tree: Tree):
        tree.assert_number_of_tips(4)


    def test_tree_is_bifurcating(tree: Tree):
        tree.assert_is_bifurcating()


    def test_outlier_branches(tree: Tree):
        # Here we create a custom function to detect outliers
        import statistics

        tips = tree.get_terminals()
        branch_lengths = [t.branch_length for t in tips]
        cut_off = statistics.mean(branch_lengths) + statistics.stdev(branch_lengths)
        for tip in tips:
            assert tip.branch_length < cut_off, f"Outlier tip '{tip.name}' (branch length = {tip.branch_length})!"

Running Phytest
################

We can then run these tests on our data with :code:`phytest`:

.. code-block:: bash

    phytest examples/example.py -s examples/data/example.fasta -t examples/data/example.tree

Generate a report by adding :code:`--report report.html`.

.. image:: https://raw.githubusercontent.com/phytest-devs/phytest/main/docs/images/report.png
    :alt: HTML Report

From the output we can see several tests failed:

.. code-block::

    FAILED examples/example.py::test_sequences_only_contains_the_characters[Sequence_B] - AssertionError: Invalid pattern found in 'Sequence_B'!
    FAILED examples/example.py::test_single_base_deletions[Sequence_C] - AssertionError: Longest stretch of '-' in 'Sequence_C' > 1!
    FAILED examples/example.py::test_longest_stretch_of_Ns_is_10[Sequence_D] - AssertionError: Longest stretch of 'N' in 'Sequence_D' > 10!
    FAILED examples/example.py::test_outlier_branches - AssertionError: Outlier tip 'Sequence_A' (branch length = 1.0)!

    Results (0.07s):
        13 passed
        4 failed
            - examples/example.py:12 test_sequences_only_contains_the_characters[Sequence_B]
            - examples/example.py:16 test_single_base_deletions[Sequence_C]
            - examples/example.py:20 test_longest_stretch_of_Ns_is_10[Sequence_D]
            - examples/example.py:32 test_outlier_branches

.. end-quickstart

See docs for more information https://phytest-devs.github.io/phytest.
