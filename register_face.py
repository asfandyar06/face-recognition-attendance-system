import cv2
import face_recognition

from config import CAMERA_INDEX, REGISTERED_FACES_DIR
from src.database import initialize_database, upsert_person
from src.face_store import ensure_face_directory, safe_filename


def main() -> None:
    initialize_database()
    ensure_face_directory()

    name = input("Enter the person's full name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    print("Press SPACE to capture. Press Q to cancel.")
    saved = False

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Failed to read from webcam.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locations = face_recognition.face_locations(rgb)
            preview = frame.copy()

            for top, right, bottom, left in locations:
                cv2.rectangle(
                    preview,
                    (left, top),
                    (right, bottom),
                    (0, 255, 0),
                    2,
                )

            cv2.putText(
                preview,
                "SPACE: save | Q: cancel",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Register Face", preview)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == 32:
                if len(locations) != 1:
                    print("Exactly one face must be visible.")
                    continue

                filename = safe_filename(name) + ".jpg"
                image_path = REGISTERED_FACES_DIR / filename

                cv2.imwrite(str(image_path), frame)
                upsert_person(name, str(image_path))

                print(f"Registered: {name}")
                saved = True
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    if not saved:
        print("Registration cancelled.")


if __name__ == "__main__":
    main()
