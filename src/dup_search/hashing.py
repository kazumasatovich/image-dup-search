from collections.abc import Sequence
from pathlib import Path

import imagehash
from PIL import Image


def phash_images(paths: Sequence[Path]) -> list[imagehash.ImageHash]:
    """pHash каждой картинки, в порядке путей"""
    hashes: list[imagehash.ImageHash] = []
    for path in paths:
        with Image.open(path) as img:
            hashes.append(imagehash.phash(img))
    return hashes
