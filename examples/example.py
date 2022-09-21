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


def test_aln_tree_match_names(alignment: Alignment, tree: Tree):
    aln_names = [i.name for i in alignment]
    tree.assert_tip_names(aln_names)


def test_any_internal_branch_lengths_above_threshold(tree: Tree, threshold=1e-4):
    tree.assert_internal_branch_lengths(min=threshold)


def test_outlier_branches(tree: Tree):
    # Here we create a custom function to detect outliers
    import statistics

    tips = tree.get_terminals()
    branch_lengths = [t.branch_length for t in tips]
    cut_off = statistics.mean(branch_lengths) + statistics.stdev(branch_lengths)
    for tip in tips:
        assert tip.branch_length < cut_off, f"Outlier tip '{tip.name}' (branch length = {tip.branch_length})!"
