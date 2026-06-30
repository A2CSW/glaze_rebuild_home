from __future__ import annotations
from services.attendance_service import create_attendance_record, list_attendance
from services.class_service import create_class
from services.enrolment_service import create_enrolment, list_enrolments
from services.link_service import link_programme_to_class, link_programme_to_product
from services.product_service import create_product, list_products
from services.programme_service import create_programme
from services.student_service import create_student
def main() -> None:
    programme = create_programme(
        name="Senior Tap",
        status="Active",
        notes="Cluster integration test",
    )
    print("Programme:", programme)
    product = create_product(
        name="Senior Tap Membership",
        programme_id=programme["programme_id"],
        status="Active",
    )
    print("Product:", product)
    dance_class = create_class(
        name="Senior Tap Thursday 6PM",
        programme_id=programme["programme_id"],
        day="Thursday",
        time="18:00",
        status="Active",
    )
    print("Class:", dance_class)
    programme_product_link = link_programme_to_product(
        programme_id=programme["programme_id"],
        product_id=product["product_id"],
    )
    print("Programme -> Product link:", programme_product_link)
    programme_class_link = link_programme_to_class(
        programme_id=programme["programme_id"],
        class_id=dance_class["class_id"],
    )
    print("Programme -> Class link:", programme_class_link)
    student = create_student(
        first_name="Katherine",
        last_name="Johnson",
        status="Current",
        notes="Programme cluster test student",
    )
    print("Student:", student)
    enrolment = create_enrolment(
        student_id=student["student_id"],
        product_id=product["product_id"],
        start_date="2026-09-01",
        enrolment_status="Active",
    )
    print("Enrolment:", enrolment)
    attendance = create_attendance_record(
        student_id=student["student_id"],
        class_id=dance_class["class_id"],
        session_date="2026-09-10",
        status="Present",
        notes="Initial attendance test",
    )
    print("Attendance:", attendance)
    print("Products rows:", len(list_products()))
    print("Enrolments rows:", len(list_enrolments()))
    print("Attendance rows:", len(list_attendance()))
if __name__ == "__main__":
    main()
