from __future__ import annotations
TABLE_RULES: dict[str, dict[str, list[str] | None]] = {
    "students": {
        "required": ["student_id", "first_name", "last_name", "status"],
        "unique_key": ["student_id"],
    },
    "guardians": {
        "required": ["guardian_id", "guardian_name"],
        "unique_key": ["guardian_id"],
    },
    "classes": {
        "required": ["class_id", "name", "status"],
        "unique_key": ["class_id"],
    },
    "programmes": {
        "required": ["programme_id", "name", "status"],
        "unique_key": ["programme_id"],
    },
    "products": {
        "required": ["product_id", "name", "status"],
        "unique_key": ["product_id"],
    },
    "programme_products": {
        "required": ["programme_product_id", "programme_id", "product_id"],
        "unique_key": ["programme_product_id"],
    },
    "programme_classes": {
        "required": ["programme_class_id", "programme_id", "class_id"],
        "unique_key": ["programme_class_id"],
    },
    "enrolments": {
        "required": ["enrolment_id", "student_id", "product_id", "enrolment_status"],
        "unique_key": ["enrolment_id"],
    },
    "attendance": {
        "required": ["attendance_id", "student_id", "class_id", "session_date", "status"],
        "unique_key": ["attendance_id"],
    },
    "bank_transactions": {
        "required": ["transaction_id", "date", "description", "amount", "review_status"],
        "unique_key": ["transaction_id"],
    },
    "payment_aliases": {
        "required": ["alias_id", "guardian_id", "alias"],
        "unique_key": ["alias_id"],
    },
    "payment_allocations": {
        "required": ["allocation_id", "transaction_id", "student_id", "amount"],
        "unique_key": ["allocation_id"],
    },
    "bank_audit": {
        "required": ["audit_id", "timestamp", "action"],
        "unique_key": ["audit_id"],
    },
}
