from __future__ import annotations
from services.class_service import create_class, list_classes
from services.programme_service import create_programme, list_programmes
from services.student_service import create_student, list_students, update_student
def main() -> None:
    created_programme = create_programme(
        name="Junior Ballet",
        status="Active",
        notes="Foundation programme",
    )
    print("Created programme:", created_programme)
    created_class = create_class(
        name="Monday Ballet 4PM",
        programme_id=created_programme["programme_id"],
        day="Monday",
        time="16:00",
        status="Active",
    )
    print("Created class:", created_class)
    created_student = create_student(
        first_name="Grace",
        last_name="Hopper",
        status="Current",
        notes="First real service-layer test",
    )
    print("Created student:", created_student)
    updated_student = update_student(
        created_student["student_id"],
        search_rule="HOPPER PAYMENT REF",
        status="Current",
    )
    print("Updated student:", updated_student)
    print("Students rows:", len(list_students()))
    print("Classes rows:", len(list_classes()))
    print("Programmes rows:", len(list_programmes()))
if __name__ == "__main__":
    main()
