from typing import List, Tuple

import cv2
import face_recognition
import numpy as np


def detect_and_encode(
    frame_bgr,
    scale: float,
) -> Tuple[List[Tuple[int, int, int, int]], List[np.ndarray]]:
    small_frame = cv2.resize(
        frame_bgr,
        (0, 0),
        fx=scale,
        fy=scale,
    )

    rgb_small_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB,
    )

    locations = face_recognition.face_locations(rgb_small_frame)
    encodings = face_recognition.face_encodings(
        rgb_small_frame,
        locations,
    )

    return locations, encodings


def best_match(
    face_encoding: np.ndarray,
    known_encodings: List[np.ndarray],
    known_names: List[str],
    tolerance: float,
) -> str:
    if not known_encodings:
        return "Unknown"

    distances = face_recognition.face_distance(
        known_encodings,
        face_encoding,
    )
    best_index = int(np.argmin(distances))

    if distances[best_index] <= tolerance:
        return known_names[best_index]

    return "Unknown"
