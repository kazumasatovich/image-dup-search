#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

from dup_search.groups import groups_search
from dup_search.hashing import phash_images
from dup_search.matrix import build_hash_matrix
from dup_search.report import groups_by_source, load_markup, sources_by_group
from dup_search.similarity_relation import similarity_relation_matrix

DATA_ENV = "DUP_SEARCH_DATA"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Делит набор на группы похожих картинок по pHash."
    )
    parser.add_argument("name", help="имя директории набора")
    parser.add_argument(
        "--r", type=int, required=True, help="порог схожести в битах: ребро, если d ≤ r"
    )
    args = parser.parse_args()
    if args.r < 0:
        parser.error("--r должно быть неотрицательным")

    data_dir = os.environ.get(DATA_ENV)
    if not data_dir:
        sys.exit(f"Ошибка: не задана переменная окружения {DATA_ENV}.")

    set_dir = Path(data_dir) / "sets" / args.name
    paths = sorted((set_dir / "images").glob("*.png"))
    if not paths:
        sys.exit(f"Ошибка: в {set_dir / 'images'} нет картинок.")
    markup_path = set_dir / "markup.csv"
    if not markup_path.exists():
        sys.exit(f"Ошибка: нет разметки {markup_path}.")

    markup = load_markup(markup_path)
    names = [path.name for path in paths]
    dist = build_hash_matrix(phash_images(paths))
    groups = groups_search(similarity_relation_matrix(dist, args.r))
    groups.sort(key=len, reverse=True)
    sources = sources_by_group(groups, names, markup)
    family_groups = groups_by_source(groups, names, markup)

    print(f"{args.name}: {len(paths)} картинок, r = {args.r}")
    print(f"Групп: {len(groups)}, из них одиночек: {sum(len(g) == 1 for g in groups)}")
    print(f"Групп из нескольких семейств: {sum(len(s) > 1 for s in sources)}")
    m = sum(len(s) > 1 for s in family_groups.values())
    print(f"Семейств в нескольких группах: {m}")

    for number, (group, families) in enumerate(zip(groups, sources, strict=True), 1):
        if len(group) == 1:
            continue
        print(f"\nГруппа {number}: {len(group)} картинок, семейств: {len(families)}")
        rows = sorted(
            (markup[names[i]] for i in group), key=lambda r: (r["source"], r["file"])
        )
        for row in rows:
            edit = f"{row['op']} {row['param']}".rstrip()
            print(f"  {row['file']}  {row['source']}  {edit}")
    print()
    print("Семейства изображений, разделившиеся в разные группы:")
    for family, gr in family_groups.items():
        if len(gr) > 1:
            print(f"{family}: в группах {sorted(group + 1 for group in gr)}")


if __name__ == "__main__":
    main()
