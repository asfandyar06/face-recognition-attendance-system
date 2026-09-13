import cv2

from config import (
    CAMERA_INDEX,
    FRAME_SCALE,
    PROCESS_EVERY_N_FRAMES,
    RECOGNITION_TOLERANCE,
)
from src.database import initialize_database, mark_attendance
from src.face_store import load_known_faces
from src.recognizer import best_match, detect_and_encode


def main() -> None:
    initialize_database()

    known_encodings, known_names = load_known_faces()

    if not known_encodings:
        print("No registered faces found. Run register_face.py first.")
        return

    print(f"Loaded {len(known_names)} registered face(s).")

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    frame_number = 0
    face_locations = []
    face_names = []
    session_marked = set()

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Failed to read webcam frame.")
                break

            frame_number += 1

            if frame_number % PROCESS_EVERY_N_FRAMES == 0:
                face_locations, encodings = detect_and_encode(
                    frame,
                    FRAME_SCALE,
                )

                face_names = []

                for encoding in encodings:
                    name = best_match(
                        encoding,
                        known_encodings,
                        known_names,
                        RECOGNITION_TOLERANCE,
                    )

                    face_names.append(name)

                    if (
                        name != "Unknown"
                        and name not in session_marked
                    ):
                        created = mark_attendance(name)

                        if created:
                            print(f"Attendance recorded: {name}")
                        else:
                            print(f"Already marked today: {name}")

                        session_marked.add(name)

            display = frame.copy()
            inverse_scale = round(1 / FRAME_SCALE)

            for (top, right, bottom, left), name in zip(
                face_locations,
                face_names,
            ):
                top = int(top * inverse_scale)
                right = int(right * inverse_scale)
                bottom = int(bottom * inverse_scale)
                left = int(left * inverse_scale)

                color = (
                    (0, 200, 0)
                    if name != "Unknown"
                    else (0, 0, 255)
                )

                cv2.rectangle(
                    display,
                    (left, top),
                    (right, bottom),
                    color,
                    2,
                )

                cv2.rectangle(
                    display,
                    (left, bottom - 35),
                    (right, bottom),
                    color,
                    cv2.FILLED,
                )

                cv2.putText(
                    display,
                    name,
                    (left + 6, bottom - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.7,
                    (255, 255, 255),
                    1,
                )

            cv2.imshow("Face Recognition Attendance", display)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
