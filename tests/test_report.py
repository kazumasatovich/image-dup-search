from pathlib import Path

from dup_search.generator import Row, write_markup
from dup_search.report import groups_by_source, load_markup, sources_by_group

# Семейства 0001.png (оригинал и три копии) и 0003.png (один оригинал)
NAMES = ["0001.png", "0002.png", "0003.png", "0004.png", "0005.png"]
MARKUP = {
    "0001.png": {"file": "0001.png", "source": "0001.png", "op": "orig"},
    "0002.png": {"file": "0002.png", "source": "0001.png", "op": "jpeg"},
    "0003.png": {"file": "0003.png", "source": "0003.png", "op": "orig"},
    "0004.png": {"file": "0004.png", "source": "0001.png", "op": "blur"},
    "0005.png": {"file": "0005.png", "source": "0001.png", "op": "crop"},
}
# Первая группа собрала два семейства, семейство 0001.png разошлось по трём группам
GROUPS = [[0, 1, 2], [3], [4]]


def test_markup_is_keyed_by_file(tmp_path: Path) -> None:
    rows = [
        Row("0002.png", "0001.png", "jpeg", 35, ""),
        Row("0001.png", "0001.png", "orig", None, "im7.jpg"),
    ]
    write_markup(rows, tmp_path / "markup.csv")
    markup = load_markup(tmp_path / "markup.csv")
    assert markup["0002.png"]["source"] == "0001.png"
    assert markup["0001.png"]["op"] == "orig"


def test_group_lists_families_of_its_images() -> None:
    assert sources_by_group(GROUPS, NAMES, MARKUP) == [
        {"0001.png", "0003.png"},
        {"0001.png"},
        {"0001.png"},
    ]


def test_sources_list_by_number_of_groups() -> None:
    assert groups_by_source(GROUPS, NAMES, MARKUP) == {
        "0001.png": {0, 1, 2},
        "0003.png": {0},
    }
