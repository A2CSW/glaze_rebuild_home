from __future__ import annotations
from services.attendance_register_service import (
    build_attendance_register,
    save_attendance_register,
)
def main() -> None:
    class_id = "CLS-7B23A777"
    session_date = "2026-09-17"
    register = build_attendance_register(class_id, session_date)
    print("Initial register:")
    print(register.to_string(index=False))
    rows = register.to_dict(orient="records")
    if rows:
        rows[0]["status"] = "Late"
        rows[0]["notes"] = "Arrived after warmup"
    saved = save_attendance_register(class_id, session_date, rows)
    print("\nSaved register:")
    print(saved.to_string(index=False))
    rebuilt = build_attendance_register(class_id, session_date)
    print("\nReloaded register:")
    print(rebuilt.to_string(index=False))
if __name__ == "__main__":
    main()
