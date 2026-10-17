import csv
import re
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from dup_search.generator import blur, build_set, crop_center, downscale, rotate


def noise(width: int, height: int, seed: int = 0) -> Image.Image:
    rng = np.random.default_rng(seed)
    pixels = rng.integers(0, 256, (height, width, 3), dtype=np.uint8)
    return Image.fromarray(pixels)


@pytest.fixture
def originals(tmp_path: Path) -> list[Path]:
    paths = [tmp_path / f"im{i}.jpg" for i in range(3)]
    for i, path in enumerate(paths):
        noise(64, 48, seed=i).save(path)
    return paths


def read_markup(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_crop_cuts_given_share_of_area() -> None:
    assert crop_center(noise(100, 50), 0.36).size == (80, 40)


def test_downscale_keeps_proportions() -> None:
    assert downscale(noise(200, 100), 0.25).size == (50, 25)


def test_rotate_by_90_loses_no_pixels() -> None:
    img = noise(40, 30)
    back = rotate(rotate(img, 90), 270)
    assert rotate(img, 90).size == (30, 40)
    assert np.array_equal(np.asarray(back), np.asarray(img))


def test_markup_lists_every_image_once(originals: list[Path], tmp_path: Path) -> None:
    out = tmp_path / "set"
    build_set(originals, out, n_copies=2, seed=1)
    rows = read_markup(out / "markup.csv")
    files = sorted(p.name for p in (out / "images").iterdir())
    assert sorted(row["file"] for row in rows) == files
    assert len(files) == 3 * (1 + 2)


def test_every_image_points_to_an_original(
    originals: list[Path], tmp_path: Path
) -> None:
    rows = build_set(originals, tmp_path / "set", n_copies=2, seed=1)
    origs = {row.file for row in rows if row.op == "orig"}
    assert len(origs) == 3
    assert all(row.source in origs for row in rows)


def test_names_do_not_reveal_edit(originals: list[Path], tmp_path: Path) -> None:
    rows = build_set(originals, tmp_path / "set", n_copies=4, seed=1)
    assert all(re.fullmatch(r"\d{4}\.png", row.file) for row in rows)


def test_same_seed_gives_same_set(originals: list[Path], tmp_path: Path) -> None:
    a = build_set(originals, tmp_path / "a", n_copies=2, seed=7)
    b = build_set(originals, tmp_path / "b", n_copies=2, seed=7)
    assert a == b


def test_existing_set_is_not_overwritten(originals: list[Path], tmp_path: Path) -> None:
    build_set(originals, tmp_path / "set", n_copies=1, seed=1)
    with pytest.raises(FileExistsError):
        build_set(originals, tmp_path / "set", n_copies=1, seed=1)


def test_blur_change_dispersion() -> None:
    assert (
        np.asarray(blur(noise(200, 300), 1)).std() < np.asarray(noise(200, 300)).std()
    )
