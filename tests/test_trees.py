from io import StringIO
from datetime import datetime
import pytest

from phytest import Tree
from phytest.utils import default_date_patterns

def test_assert_tree_number_of_tips():
    treedata = "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    handle = StringIO(treedata)
    tree = Tree.read(handle, "newick")
    tree.assert_number_of_tips(tips=7, min=6, max=8)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(tips=1)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(min=8)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(max=6)


def test_assert_tree_is_bifurcating():
    treedata = "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    handle = StringIO(treedata)
    tree = Tree.read(handle, "newick")
    tree.assert_is_bifurcating()


def test_assert_tree_total_branch_length():
    treedata = "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):1):1):1, Rodent:1);"
    handle = StringIO(treedata)
    tree = Tree.read(handle, "newick")
    tree.assert_total_branch_length(length=11, min=10, max=12)
    with pytest.raises(AssertionError):
        tree.assert_total_branch_length(length=1)
    with pytest.raises(AssertionError):
        tree.assert_total_branch_length(min=12)
    with pytest.raises(AssertionError):
        tree.assert_total_branch_length(max=10)


def test_assert_tip_regex():
    tree = Tree.read_str("(A_1993.3, (B_1998-07-02,C_1992-12-31));")
    patterns = default_date_patterns()

    # Since the tree uses both conventions, just asserting a single pattern should fail
    for pattern in patterns:
        with pytest.raises(AssertionError):
            tree.assert_tip_regex(pattern)
    
    # Giving both patterns should pass
    tree.assert_tip_regex(patterns)


def test_parse_tip_dates():
    tree = Tree.read_str("(A_1993.3, (B_1998-07-02,C_1992-10-01));")
    dates = tree.parse_tip_dates()
    assert dates == {
        'A_1993.3': datetime(1993, 4, 20, 0, 0),
        'B_1998-07-02': datetime(1998, 7, 2, 0, 0),
        'C_1992-10-01': datetime(1992, 10, 1, 0, 0),
    }
    dates = tree.parse_tip_dates(decimal_year=True)
    assert dates == {
        'A_1993.3': 1993.3,
        'B_1998-07-02': 1998.5,
        'C_1992-10-01': 1992.75,
    }


def test_assert_root_to_tip():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    tree.assert_root_to_tip(min_r_squared=0.35)
    with pytest.raises(AssertionError):
        tree.assert_root_to_tip(min_r_squared=0.40)

    tree.assert_root_to_tip(min_rate=1.5e-03, max_rate=1.6e-03)
    with pytest.raises(AssertionError):
        tree.assert_root_to_tip(max_rate=1.5e-03)
    with pytest.raises(AssertionError):
        tree.assert_root_to_tip(min_rate=1.6e-03)

