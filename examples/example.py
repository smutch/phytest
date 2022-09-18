from phytest import Alignment, Sequence, Tree

from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
import warnings
import pytest
from phytest import Tree
from phytest.utils import PhytestAssertion, PhytestWarning, default_date_patterns


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

def test_aln_tree_match_names(alignment: Alignment, tree : Tree):
    tree_names = [i.name for i in tree.get_terminals()]
    aln_names = [i.name for i in alignment]
    have_same_number_of_taxa = len(tree_names) == len(aln_names)
    all_aln_names_in_tree = all([i in aln_names for i in tree_names])
    assert have_same_number_of_taxa and all_aln_names_in_tree

def test_any_internal_branch_lengths_below_threshold(tree: Tree, threshold = 1e-4):
    branch_lengths_below_threshold = [i.branch_length >= threshold for i in tree.get_nonterminals()[1:]]
    assert all(branch_lengths_below_threshold)
