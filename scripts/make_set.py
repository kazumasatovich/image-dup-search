#!/usr/bin/env python3
import argparse
import os
import random
import sys
from pathlib import Path

from dup_search.generator import EDITS, build_set

DATA_ENV = "DUP_SEARCH_DATA"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Собирает набор: оригиналы из MIRFLICKR, их копии и разметку."
    )
    parser.add_argument("name", help="имя набора, например set100")
    parser.add_argument("--originals", type=int, default=20, help="число оригиналов")
    parser.add_argument(
        "--copies",
        type=int,
        default=4,
        help=f"копий на оригинал, от 0 до {len(EDITS)}",
    )
    parser.add_argument("--seed", type=int, default=0, help="зерно случайного выбора")
    args = parser.parse_args()
    if not 0 <= args.copies <= len(EDITS):
        parser.error(f"--copies должно быть от 0 до {len(EDITS)}")

    data_dir = os.environ.get(DATA_ENV)
    if not data_dir:
        sys.exit(f"Ошибка: не задана переменная окружения {DATA_ENV}.")

    source_dir = Path(data_dir) / "mirflickr"
    pool = sorted(source_dir.rglob("*.jpg"))
    if len(pool) < args.originals:
        sys.exit(f"Ошибка: в {source_dir} {len(pool)} картинок из {args.originals}.")

    originals = random.Random(args.seed).sample(pool, args.originals)
    out_dir = Path(data_dir) / "sets" / args.name
    try:
        rows = build_set(originals, out_dir, args.copies, args.seed)
    except FileExistsError:
        sys.exit(f"Ошибка: набор {out_dir} уже есть. Удалите его или смените имя.")

    print(f"Готово: {len(rows)} картинок в {out_dir / 'images'}")
    print(f"Разметка: {out_dir / 'markup.csv'}")


if __name__ == "__main__":
    main()
