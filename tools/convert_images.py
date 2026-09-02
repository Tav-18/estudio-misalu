from pathlib import Path
from PIL import Image, ImageOps

IMG_DIR = (
    Path(__file__).resolve().parent.parent
    / "core"
    / "static"
    / "core"
    / "img"
)

EXTENSIONS = {".jpg", ".jpeg", ".png"}

for source in IMG_DIR.rglob("*"):
    if not source.is_file():
        continue

    if source.suffix.lower() not in EXTENSIONS:
        continue

    destination = source.with_suffix(".webp")

    try:
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

        print(
            f"OK: {source.relative_to(IMG_DIR)} "
            f"-> {destination.relative_to(IMG_DIR)}"
        )

    except Exception as error:
        print(
            f"ERROR: {source.relative_to(IMG_DIR)} "
            f"-> {error}"
        )