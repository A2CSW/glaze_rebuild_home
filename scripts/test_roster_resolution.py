from __future__ import annotations
from services.roster_service import resolve_class_roster
def main() -> None:
    roster = resolve_class_roster("CLS-7B23A777")
    print("Roster rows:", len(roster))
    print(roster.to_string(index=False))
if __name__ == "__main__":
    main()
