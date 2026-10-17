"""Генератор изменённых копий и разметки к ним.

Каждая копия — одна правка оригинала: имя правки op и её параметр param.

    op          param
    jpeg        качество при пересжатии в JPEG
    scale       доля исходной стороны после уменьшения
    crop        доля отрезанной площади; кроп по центру, пропорции сохраняются
    brightness  множитель яркости, 1 — без изменений
    rotate      угол поворота против часовой стрелки, в градусах
    blur        радиус размытия по каусу в пикселях

Разметка — markup.csv, по строке на каждую картинку набора:

    file    имя картинки в наборе: номер без смысла, например 0042.png
    source  имя оригинала, из которого сделана картинка; у оригинала — своё
    op      правка; у оригинала — orig
    param   параметр правки; у оригинала пусто
    origin  имя исходного файла MIRFLICKR; только у оригиналов

Метку о дубле генератор ставить не будет, ее установим, с помощью функции сравнения

Все картинки сохраняются в PNG.
"""

import csv
import io
import math
import random
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


def recompress_jpeg(img: Image.Image, quality: float) -> Image.Image:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=int(quality))
    with Image.open(buf) as out:
        return out.convert("RGB")


def downscale(img: Image.Image, share: float) -> Image.Image:
    size = (max(1, round(img.width * share)), max(1, round(img.height * share)))
    return img.resize(size, Image.Resampling.LANCZOS)


def crop_center(img: Image.Image, cut: float) -> Image.Image:
    k = math.sqrt(1 - cut)
    width, height = max(1, round(img.width * k)), max(1, round(img.height * k))
    left, top = (img.width - width) // 2, (img.height - height) // 2
    return img.crop((left, top, left + width, top + height))


def change_brightness(img: Image.Image, factor: float) -> Image.Image:
    return ImageEnhance.Brightness(img).enhance(factor)


def rotate(img: Image.Image, angle: float) -> Image.Image:
    if angle % 90 == 0:
        return img.rotate(angle, expand=True)
    return img.rotate(angle, resample=Image.Resampling.BICUBIC)


def blur(img: Image.Image, radius: float) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(radius))


@dataclass(frozen=True)
class Edit:
    apply: Callable[[Image.Image, float], Image.Image]
    sample: Callable[[random.Random], float]


ANGLES = [*range(1, 360)]

EDITS: dict[str, Edit] = {
    "jpeg": Edit(recompress_jpeg, lambda rng: rng.randint(10, 90)),
    "scale": Edit(downscale, lambda rng: round(rng.uniform(0.25, 0.9), 3)),
    "crop": Edit(crop_center, lambda rng: round(rng.uniform(0.05, 0.5), 3)),
    "brightness": Edit(change_brightness, lambda rng: round(rng.uniform(0.5, 1.5), 3)),
    "rotate": Edit(rotate, lambda rng: rng.choice(ANGLES)),
    "blur": Edit(blur, lambda rng: round(rng.uniform(0.5, 3.0))),
}


@dataclass(frozen=True)
class Row:
    file: str
    source: str
    op: str
    param: float | None
    origin: str


def build_set(
    originals: Sequence[Path], out_dir: Path, n_copies: int, seed: int
) -> list[Row]:
    if not 0 <= n_copies <= len(EDITS):
        raise ValueError(f"n_copies должно быть от 0 до {len(EDITS)}")

    rng = random.Random(seed)
    images_dir = out_dir / "images"
    images_dir.mkdir(parents=True)

    total = len(originals) * (1 + n_copies)
    width = max(4, len(str(total)))
    # Случайные номера, чтобы не задавать естественную разметку
    numbers = iter(rng.sample(range(1, total + 1), total))

    rows: list[Row] = []
    for path in originals:
        with Image.open(path) as src:
            img = src.convert("RGB")
        orig = f"{next(numbers):0{width}d}.png"
        img.save(images_dir / orig)
        rows.append(Row(orig, orig, "orig", None, path.name))

        for op in rng.sample(sorted(EDITS), n_copies):
            param = EDITS[op].sample(rng)
            name = f"{next(numbers):0{width}d}.png"
            EDITS[op].apply(img, param).save(images_dir / name)
            rows.append(Row(name, orig, op, param, ""))

    write_markup(rows, out_dir / "markup.csv")
    return rows


def write_markup(rows: Sequence[Row], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[field.name for field in fields(Row)])
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
