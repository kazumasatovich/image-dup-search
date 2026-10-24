from pathlib import Path

import numpy as np
from PIL import Image

from dup_search.hashing import phash_images


def picture(seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    cells = rng.integers(0, 256, (8, 8), dtype=np.uint8)
    return Image.fromarray(cells).resize((64, 64), Image.Resampling.BILINEAR)


def test_each_hash_belongs_to_its_path(tmp_path: Path) -> None:
    a, a_copy, b = tmp_path / "a.png", tmp_path / "a_copy.png", tmp_path / "b.png"
    picture(0).save(a)
    picture(0).save(a_copy)
    picture(1).save(b)
    hashes = phash_images([a, a_copy, b])
    assert hashes[0] - hashes[1] == 0
    assert hashes[0] - hashes[2] > 0
