#!/usr/bin/env python3
import argparse
import os
import sys

import imagehash
from PIL import Image

from dup_search.matrix import build_hash_matrix, print_as_matrix
from dup_search.similarity_relation import (
    print_relation_matrix,
    similarity_relation_matrix,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Путь к исходному изображению")
    parser.add_argument(
        "threshold",
        help="Порог расстояния Хэмминга," " при котором расстояния считаюся похожими",
    )
    args = parser.parse_args()

    input_path = args.image_path
    threshold = int(args.threshold)

    if not os.path.exists(input_path):
        print(f"Ошибка: файл '{input_path}' не найден.")
        sys.exit(1)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    angles = [0, 3, 6, 9, 12, 15]

    hashes = []
    filenames = []

    try:
        with Image.open(input_path) as src:
            img = src.convert("RGB")

            base_name = os.path.splitext(os.path.basename(input_path))[0]
            ext = os.path.splitext(input_path)[1]

            for angle in angles:
                rotated = img.rotate(angle, expand=False)

                out_name = f"{base_name}_rot{angle}{ext}"
                out_path = os.path.join(output_dir, out_name)

                rotated.save(out_path)
                print(f"Сохранено: {out_path}")

                h = imagehash.phash(rotated)
                hashes.append(h)
                filenames.append(f"{angle}")
    except Exception as e:
        print(f"Ошибка при обработке изобраения: {e}")
        sys.exit(1)

    matr = build_hash_matrix(hashes)
    print_as_matrix(matr)
    sim_matr = similarity_relation_matrix(matr, threshold)
    print_relation_matrix(sim_matr, angles)


if __name__ == "__main__":
    main()
