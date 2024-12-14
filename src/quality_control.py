from difflib import SequenceMatcher
from itertools import combinations
from typing import List, Set, Tuple


def _compute_ratcliff_obershelp(rationale_1: str, rationale_2: str) -> float:
    """
    Computes the Ratcliff-Obershelp similarity between a pair of rationales.
    :param rationale_1: first rationale in the pair
    :param rationale_2: second rationale in the pair
    :return: the maximum of the two similarity-scores (as RO is not commutative)
    """  # noqa: E501
    res_12: float = SequenceMatcher(
        lambda x: x in " \t\n", rationale_1, rationale_2, autojunk=False
    ).ratio()
    res_21: float = SequenceMatcher(
        lambda x: x in " \t\n", rationale_2, rationale_1, autojunk=False
    ).ratio()
    return max(res_12, res_21)


def _select_threshold(rationale_combinations: List[Tuple[str, str]]) -> float:
    """
    Computes the threshold to be used during threshold-filtering for the given data instance (AR1 paper).
    :param rationale_combinations: pairwise combinations of rationales
    :return: the dynamically-computed threshold
    """  # noqa: E501
    threshold = 0.0
    for tup in rationale_combinations:
        threshold = max(threshold, _compute_ratcliff_obershelp(tup[0], tup[1]))
    return threshold


def _filter_by_threshold(metric_inputs: List[Tuple[float, str]]) -> List[float]:
    """
    Filters the workers' input for a given metric and data instance based on rationale-overlap (AR1 paper).
    :param metric_inputs: the scores and rationales provided by the workers for the given metric and data instance
    :return: the scores for which rationale-overlap was on or above the threshold
    """  # noqa: E501
    included_indices: Set[int] = set()

    rationale_combinations: List[Tuple[str, str]] = list(
        combinations(map(lambda tup: tup[1], metric_inputs), 2)
    )
    selected_threshold: float = _select_threshold(rationale_combinations)

    for rationale_1, rationale_2 in rationale_combinations:
        if _compute_ratcliff_obershelp(rationale_1, rationale_2) >= selected_threshold:
            idx_1: int = metric_inputs.index(
                list(filter(lambda tup: tup[1] == rationale_1, metric_inputs))[0]
            )
            idx_2: int = metric_inputs.index(
                list(filter(lambda tup: tup[1] == rationale_2, metric_inputs))[0]
            )
            included_indices.add(idx_1)
            included_indices.add(idx_2)

    return [
        metric_inputs[idx][0]
        for idx in range(len(metric_inputs))
        if idx in included_indices
    ]


def aggregate_scores(
    worker_inputs: List[Tuple[float, str, float, str]]
) -> Tuple[float, float]:
    """
    Computes the aggregated performance-metrics for a given data instance via majority vote.
    :param worker_inputs: all inputs provided by the workers for the given data instance
    :return: the aggregated faithfulness- and relevancy-scores
    """  # noqa: E501
    filtered_faithfulness_vals: List[float] = _filter_by_threshold(
        list(map(lambda tup: (tup[0], tup[1]), worker_inputs))
    )
    filtered_relevancy_vals: List[float] = _filter_by_threshold(
        list(map(lambda tup: (tup[2], tup[3]), worker_inputs))
    )

    majority_faithfulness_score: float = (
        1.0
        if filtered_faithfulness_vals.count(1.0) > (len(filtered_faithfulness_vals) / 2)
        else 0.0
    )
    majority_relevancy_score: float = (
        1.0
        if filtered_relevancy_vals.count(1.0) > (len(filtered_relevancy_vals) / 2)
        else 0.0
    )

    return majority_faithfulness_score, majority_relevancy_score
