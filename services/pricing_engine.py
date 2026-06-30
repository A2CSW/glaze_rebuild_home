PRICING = {
    "core_single": 35,
    "core_dual": 60,

    "sibling": {
        1: 35,
        2: 30,
        3: 25
    },

    "showreel": 12,
    "showreel_bundle": 30,

    "summer_shoot": 110,

    "short_course_single": 100,
    "short_course_pass": 255,

    "summer_camp_member": 178,
    "summer_camp_non_member": 198,
    "ultimate_summer_bundle": 255
}


def get_core_fee(student):
    if student.get("classes") == "dual":
        return PRICING["core_dual"]
    return PRICING["core_single"]


def get_sibling_fee(student):
    group = student.get("siblings_group", 1)
    return PRICING["sibling"].get(group, PRICING["core_single"])


def calculate_student_price(student):
    """
    Fully expanded pricing model (no payments involved yet)
    """

    breakdown = {}

    # Core class
    core = get_core_fee(student)
    breakdown["core"] = core

    # Sibling adjustment override (if present)
    if "siblings_group" in student:
        breakdown["sibling_adjusted_core"] = get_sibling_fee(student)

    # Showreels
    showreels = student.get("showreels", 0)
    if showreels == 3:
        breakdown["showreels"] = PRICING["showreel_bundle"]
    else:
        breakdown["showreels"] = showreels * PRICING["showreel"]

    # Summer shoot
    if student.get("summer_shoot"):
        breakdown["summer_shoot"] = PRICING["summer_shoot"]

    # Short course pass
    if student.get("short_course_pass"):
        breakdown["short_course"] = PRICING["short_course_pass"]

    # Summer camp
    if student.get("summer_camp"):
        breakdown["summer_camp"] = PRICING["summer_camp_member"]

    total = sum(breakdown.values())

    return {
        "student_id": student["student_id"],
        "breakdown": breakdown,
        "total": total
    }
