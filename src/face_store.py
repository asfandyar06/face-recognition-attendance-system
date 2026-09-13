from typing import List, Tuple

import face_recognition
import numpy as np

from config import REGISTERED_FACES_DIR


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def ensure_face_directory() -> None:
    REGISTERED_FACES_DIR.mkdir(parents=True, exist_ok=True)


def safe_filename(name: str) -> str:
    cleaned = "".join(
        ch for ch in name.strip()
        if ch.isalnum() or ch in {" ", "-", "_"}
    ).strip()
    return (cleaned.replace(" ", "_") or "person")


def load_known_faces() -> Tuple[List[np.ndarray], List[str]]:
    ensure_face_directory()

    encodings = []
    names = []

    for image_path in sorted(REGISTERED_FACES_DIR.iterdir()):
        if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        image = face_recognition.load_image_file(str(image_path))
        found = face_recognition.face_encodings(image)

        if len(found) != 1:
            print(
                f"[WARN] Skipping {image_path.name}: "
                f"expected 1 face, found {len(found)}."
            )
            continue

        encodings.append(found[0])
        names.append(image_path.stem.replace("_", " "))

    return encodings, names
