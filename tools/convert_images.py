from pathlib import Path
from PIL import Image, ImageOps

IMG_DIR = Path(__file__).resolve().parent.parent / "core" / "static" / "core" / "img"

NAMES = [
    "hero-misalu",
    "urbano",
    "contemporaneo",
    "kpop",
    "galeria-01",
    "galeria-02",
    "galeria-03",
    "galeria-04",
]

EXTENSIONS = [".jpg", ".jpeg", ".png"]

for name in NAMES:
    source = None

    for extension in EXTENSIONS:
        possible = IMG_DIR / f"{name}{extension}"

        if possible.exists():
            source = possible
            break

    if source is None:
        print(f"NO ENCONTRADA: {name}")
        continue

    destination = IMG_DIR / f"{name}.webp"

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        image.thumbnail((1920, 1920))

        image.save(
            destination,
            "WEBP",
            quality=86,
            method=6,
        )

    print(f"OK: {source.name} -> {destination.name}")