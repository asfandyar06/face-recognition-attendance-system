# Face Recognition Attendance System

A reusable Python attendance system that identifies registered users with a webcam and records attendance in SQLite.

> **Privacy note:** Facial recognition uses biometric information. Only enroll people with their explicit consent, keep the data secure, and follow applicable privacy/data-protection rules.

## Features

- Webcam-based face registration
- Real-time face recognition
- SQLite attendance database
- Prevents duplicate attendance on the same day
- CSV export
- Configurable recognition tolerance
- Clean modular structure
- Easy to extend with a web dashboard or API

## Project Structure

```text
face-recognition-attendance-system/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config.py
├── register_face.py
├── run_attendance.py
├── export_attendance.py
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── face_store.py
│   └── recognizer.py
├── data/
│   └── registered_faces/
└── screenshots/
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/face-recognition-attendance-system.git
cd face-recognition-attendance-system
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## Register a User

```bash
python register_face.py
```

Enter the person's name, look at the camera, and press `SPACE` to save. Press `Q` to cancel.

## Run Attendance

```bash
python run_attendance.py
```

Press `Q` to close the webcam.

## Export Attendance

```bash
python export_attendance.py
```

This creates `attendance_export.csv`.

## Privacy / Security Recommendations

Before production deployment:

- obtain explicit consent before enrollment
- restrict access to biometric data
- encrypt backups and storage where appropriate
- define a data-retention policy
- allow users to request deletion
- add liveness / anti-spoofing checks
- use authentication for administrative tools
- avoid committing real face images to GitHub

The included `.gitignore` prevents registered faces and local databases from being committed accidentally.

## Future Improvements

- Web dashboard
- Role-based authentication
- PostgreSQL/MySQL support
- REST API
- Multi-camera support
- Attendance analytics
- Liveness detection
- Docker support

## License

MIT
