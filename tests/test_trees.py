import warnings
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from phytest import Tree
from phytest.utils import PhytestAssertion, PhytestWarning, default_date_patterns


def test_assert_tree_number_of_tips():
    tree = Tree.read_str(
        "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    )
    tree.assert_number_of_tips(tips=7, min=6, max=8)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(tips=1)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(min=8)
    with pytest.raises(AssertionError):
        tree.assert_number_of_tips(max=6)


def test_assert_unique_tips():
    tree = Tree.read_str(
        "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    )
    tree.assert_unique_tips()
    tree = Tree.read_str(
        "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Bovine:1.21460);"
    )
    with pytest.raises(AssertionError):
        tree.assert_unique_tips()


def test_assert_tree_is_rooted():
    tree = Tree.read_str("((A:0.1,B:0.2):0.3,(C:0.3,D:0.4):0.5);")
    with pytest.raises(AssertionError):
        tree.assert_is_rooted()
    tree.root_at_midpoint()
    tree.assert_is_rooted()


def test_assert_tree_is_bifurcating():
    tree = Tree.read_str(
        "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    )
    tree.assert_is_bifurcating()


def test_assert_tree_is_monophyletic():
    tree = Tree.read_str(
        "(Bovine:0.69395,(Hylobates:0.36079,(Pongo:0.33636,(G._Gorilla:0.17147, (P._paniscus:0.19268,H._sapiens:0.11927):0.08386):0.06124):0.15057):0.54939, Rodent:1.21460);"
    )
    print(tree.root)
    tips = [tip for tip in tree.get_terminals() if tip.name in ("P._paniscus", "H._sapiens")]
    tree.assert_is_monophyletic(tips)
    with pytest.raises(AssertionError):
        tips = [tip for tip in tree.get_terminals() if tip.name in ("Pongo", "H._sapiens")]
        tree.assert_is_monophyletic(tips)


def test_assert_branch_lengths():
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):1):1):1, Rodent:1);"
    )
    tree.assert_branch_lengths(min=0, max=1)
    with pytest.raises(AssertionError):
        tree.assert_branch_lengths(min=2)
    with pytest.raises(AssertionError):
        tree.assert_branch_lengths(max=0)


def test_assert_no_negative_branch_lengths():
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):1):1):1, Rodent:1);"
    )
    tree.assert_no_negatives()
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):-1):1):1):1, Rodent:1);"
    )
    with pytest.raises(AssertionError):
        tree.assert_no_negatives()


def test_assert_terminal_branch_lengths():
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):5):1):1, Rodent:1);"
    )
    tree.assert_terminal_branch_lengths(min=0, max=1)
    with pytest.raises(AssertionError):
        tree.assert_terminal_branch_lengths(min=2)
    with pytest.raises(AssertionError):
        tree.assert_terminal_branch_lengths(max=0)


def test_assert_internal_branch_lengths():
    tree = Tree.read_str(
        "(Bovine:4,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):2):2):2):2, Rodent:1);"
    )
    tree.assert_internal_branch_lengths(min=0, max=2)
    with pytest.raises(AssertionError):
        tree.assert_internal_branch_lengths(min=3)
    with pytest.raises(AssertionError):
        tree.assert_internal_branch_lengths(max=1)


def test_assert_tree_total_branch_length():
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):1):1):1, Rodent:1);"
    )
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


def test_assert_tip_names():
    tree = Tree.read_str(
        "(Bovine:1,(Hylobates:1,(Pongo:1,(G._Gorilla:1, (P._paniscus:1,H._sapiens:1):1):1):1):1, Rodent:1);"
    )
    tree.assert_tip_names(names=['Bovine', 'Hylobates', 'Pongo', 'G._Gorilla', 'P._paniscus', 'H._sapiens', 'Rodent'])
    with pytest.raises(AssertionError):
        tree.assert_tip_names(
            names=['Bovine', 'Bovine', 'Hylobates', 'Pongo', 'G._Gorilla', 'P._paniscus', 'H._sapiens', 'Rodent']
        )
    with pytest.raises(AssertionError):
        tree.assert_tip_names(
            names=['Different', 'Hylobates', 'Pongo', 'G._Gorilla', 'P._paniscus', 'H._sapiens', 'Rodent']
        )


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
    # Setting pattern explicitly
    dates = tree.parse_tip_dates(patterns=r"\d{4}\.?\d*$", decimal_year=True)
    assert dates == {
        'A_1993.3': 1993.3,
    }


def test_plot_root_to_tip():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    with NamedTemporaryFile(suffix=".svg") as file:
        path = Path(file.name)
        tree.plot_root_to_tip(path, covariation=True, sequence_length=463)
        assert path.exists()
        assert path.stat().st_size > 30_000
        svg = path.read_text()
        assert "!DOCTYPE svg PUBLIC" in svg


def test_assert_root_to_tip_min_r_squared():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    tree.assert_root_to_tip(min_r_squared=0.35)
    with pytest.raises(PhytestAssertion):
        tree.assert_root_to_tip(min_r_squared=0.40)


def test_assert_root_to_tip_rate():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    tree.assert_root_to_tip(min_rate=1.5e-03, max_rate=1.6e-03)
    with pytest.raises(PhytestAssertion):
        tree.assert_root_to_tip(max_rate=1.5e-03)
    with pytest.raises(PhytestAssertion):
        tree.assert_root_to_tip(min_rate=1.6e-03)


def test_assert_root_to_tip_root_date():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")

    tree.assert_root_to_tip(min_root_date=1772.0, max_root_date=1773.0)
    with pytest.raises(PhytestAssertion):
        tree.assert_root_to_tip(max_root_date=1772.0)
    with pytest.raises(
        PhytestAssertion, match=r"Inferred root date '1772.\d*' is less than the minimum allowed root date '1773.0'."
    ):
        tree.assert_root_to_tip(min_root_date=1773.0)

    with pytest.warns(
        PhytestWarning, match=r"Inferred root date '1772.\d*' is less than the minimum allowed root date '1773.0'."
    ):
        tree.warn_root_to_tip(min_root_date=1773.0)


def test_assert_root_to_tip_covariation():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    tree.assert_root_to_tip(covariation=True, sequence_length=463, valid_confidence=True)
    tree.assert_root_to_tip(valid_confidence=False)
    with pytest.raises(PhytestAssertion, match=r"The `clock_model.valid_confidence` variable is not False."):
        tree.assert_root_to_tip(covariation=True, sequence_length=463, valid_confidence=False)

    with pytest.raises(
        PhytestAssertion,
        match=r"Cannot perform root-to-tip regression with `covariation` as True if no alignment of sequence length is provided.",
    ):
        tree.assert_root_to_tip(covariation=True, valid_confidence=True)


def test_assert_root_to_tip_root_extra():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")

    extra = []
    tree.assert_root_to_tip(min_root_date=1772.0, max_root_date=1773.0, extra=extra)
    assert extra[0]['format_type'] == 'html'
    assert extra[0]['content'].startswith('<?xml version="1.0" encoding="utf-8" standalone="no"?>')


def test_assert_root_to_tip_clock_filter():
    tree = Tree.read("examples/data/ice_viruses.fasta.treefile", tree_format="newick")
    with pytest.warns(PhytestWarning):
        tree.assert_root_to_tip(clock_filter=1.0)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        tree.assert_root_to_tip(clock_filter=3.0)
