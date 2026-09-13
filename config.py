from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REGISTERED_FACES_DIR = DATA_DIR / "registered_faces"
DATABASE_PATH = DATA_DIR / "attendance.db"

CAMERA_INDEX = 0
RECOGNITION_TOLERANCE = 0.48
FRAME_SCALE = 0.25
PROCESS_EVERY_N_FRAMES = 2
