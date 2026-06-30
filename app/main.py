from __future__ import annotations
import streamlit as st
from config.settings import APP_NAME, APP_VERSION, ensure_directories
from core.logging_config import get_logger
from ui.pages.intake_page import render_intake_page
from ui.pages.attendance_page import render_attendance_page
from ui.pages.bank_page import render_bank_page
from ui.pages.classes_page import render_classes_page
from ui.pages.enrolments_page import render_enrolments_page
from ui.pages.guardians_page import render_guardians_page
from ui.pages.payment_aliases_page import render_payment_aliases_page
from ui.pages.products_page import render_products_page
from ui.pages.programme_links_page import render_programme_links_page
from ui.pages.programmes_page import render_programmes_page
from ui.pages.roster_diagnostics_page import render_roster_diagnostics_page
from ui.pages.students_page import render_students_page
from ui.pages.import_forms_page import render_import_forms_page
logger = get_logger(__name__)
def render_home() -> None:
    st.title(f"{APP_NAME} - Rebuild")
    st.caption(f"Version {APP_VERSION}")
    st.write("Clean rebuild of the GLAZE operations platform.")
    st.info("Backend-first rebuild with progressively restored UI modules.")
    st.markdown(
        """
        ### Current modules
        - Students
        - Guardians
        - Programmes
        - Products
        - Classes
        - Programme Links
        - Enrolments
        - Payment Aliases
        - Attendance Register
        - Roster Diagnostics
        - Bank Transactions
        ### Current status
        - Backend validation is active
        - Backups are created before saves
        - Attendance is roster-driven
        - Guardian + alias + bank foundation is now being restored
        """
    )
def main() -> None:
    ensure_directories()
    st.set_page_config(
        page_title=f"{APP_NAME} Rebuild",
        layout="wide",
    )
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Intake",
            "Students",
            "Guardians",
            "Programmes",
            "Products",
            "Classes",
            "Enrolments",
            "Attendance",
            "Roster Diagnostics",
            "Bank Transactions",
        ],
    )

    if page == "Home":
        render_home()
    elif page == "Intake":
        render_intake_page()
    elif page == "Students":
        render_students_page()
    elif page == "Guardians":
        render_guardians_page()
    elif page == "Programmes":
        render_programmes_page()
    elif page == "Products":
        render_products_page()
    elif page == "Classes":
        render_classes_page()
    elif page == "Programme Links":
        render_programme_links_page()
    elif page == "Enrolments":
        render_enrolments_page()
    elif page == "Payment Aliases":
        render_payment_aliases_page()
    elif page == "Attendance":
        render_attendance_page()
    elif page == "Roster Diagnostics":
        render_roster_diagnostics_page()
    elif page == "Bank Transactions":
        render_bank_page()
    logger.info("Rendered page: %s", page)
if __name__ == "__main__":
    main()
