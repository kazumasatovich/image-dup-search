import csv
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path

Markup = dict[str, dict[str, str]]


def load_markup(path: Path) -> Markup:
    """Строки markup.csv по имени картинки"""
    with path.open(newline="", encoding="utf-8") as f:
        return {row["file"]: row for row in csv.DictReader(f)}


def sources_by_group(
    groups: Sequence[Sequence[int]], names: Sequence[str], markup: Markup
) -> list[set[str]]:
    """Семейства каждой группы"""
    return [{markup[names[i]]["source"] for i in group} for group in groups]


def groups_by_source(
    groups: Sequence[Sequence[int]], names: Sequence[str], markup: Markup
) -> dict[str, set[int]]:
    groups_by_source = defaultdict(set)
    for number, group in enumerate(groups):
        for image in group:
            groups_by_source[markup[names[image]]["source"]].add(number)
    return groups_by_source
