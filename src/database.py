import csv
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from config import DATABASE_PATH


def get_connection(db_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                image_path TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                attendance_date TEXT NOT NULL,
                attendance_time TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                FOREIGN KEY (person_id) REFERENCES people(id),
                UNIQUE(person_id, attendance_date)
            )
            """
        )


def upsert_person(name: str, image_path: str) -> int:
    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO people (name, image_path, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                image_path = excluded.image_path
            """,
            (name, image_path, now),
        )

        row = conn.execute(
            "SELECT id FROM people WHERE name = ?",
            (name,),
        ).fetchone()

        return int(row["id"])


def get_person_id(name: str) -> Optional[int]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM people WHERE name = ?",
            (name,),
        ).fetchone()

    return int(row["id"]) if row else None


def mark_attendance(name: str) -> bool:
    person_id = get_person_id(name)
    if person_id is None:
        return False

    today = date.today().isoformat()
    now = datetime.now()

    with get_connection() as conn:
        try:
            conn.execute(
                """
                INSERT INTO attendance (
                    person_id,
                    attendance_date,
                    attendance_time,
                    recorded_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    person_id,
                    today,
                    now.strftime("%H:%M:%S"),
                    now.isoformat(timespec="seconds"),
                ),
            )
            return True
        except sqlite3.IntegrityError:
            return False


def export_attendance_to_csv(output_path: Path) -> Path:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                people.name,
                attendance.attendance_date,
                attendance.attendance_time,
                attendance.recorded_at
            FROM attendance
            JOIN people ON people.id = attendance.person_id
            ORDER BY attendance.attendance_date DESC,
                     attendance.attendance_time DESC
            """
        ).fetchall()

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "date", "time", "recorded_at"])

        for row in rows:
            writer.writerow(
                [
                    row["name"],
                    row["attendance_date"],
                    row["attendance_time"],
                    row["recorded_at"],
                ]
            )

    return output_path
