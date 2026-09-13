from pathlib import Path

from src.database import export_attendance_to_csv, initialize_database


def main() -> None:
    initialize_database()

    output = Path("attendance_export.csv")
    created = export_attendance_to_csv(output)

    print(f"Attendance exported to: {created.resolve()}")


if __name__ == "__main__":
    main()
