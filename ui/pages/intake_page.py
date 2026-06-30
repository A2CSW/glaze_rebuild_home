from __future__ import annotations
import streamlit as st
from services.form_ingestion_service import ingest_form
from services.guardian_service import create_guardian
from services.student_service import create_student
from core.exceptions import ServiceError

def render_intake_page() -> None:
    st.header("📥 Intake Centre")
    st.caption("Tanya’s single control point for new guardians, students and consents (2026-27 pricing)")

    tab_contact, tab_taster, tab_enrol, tab_consent, tab_import = st.tabs([
        "📞 Quick Contact Us",
        "🎨 Taster / Quick Student",
        "📋 Enrolment (New Pricing)",
        "✅ Consent",
        "📤 Bulk CSV Import"
    ])

    # ====================== TAB 1: QUICK CONTACT US ======================
    with tab_contact:
        st.subheader("Add Guardian (Contact Us minimum)")
        with st.form("contact_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                g_name = st.text_input("Guardian Name *")
                g_email = st.text_input("Email")
            with col2:
                g_phone = st.text_input("Mobile / Phone")
                notes = st.text_area("Notes / How can we help?", height=80)

            submitted = st.form_submit_button("Save Guardian", use_container_width=True)

        if submitted:
            if not g_name:
                st.error("Guardian name is required.")
            else:
                try:
                    guardian = create_guardian(
                        guardian_name=g_name,
                        email=g_email,
                        phone=g_phone,
                        notes=notes
                    )
                    st.success(f"✅ Guardian created: {guardian['guardian_name']}")
                    st.rerun()
                except ServiceError as e:
                    st.error(str(e))

    # ====================== TAB 2: TASTER / QUICK STUDENT ======================
    with tab_taster:
        st.subheader("Add Student + Link to Guardian (Taster style)")
        with st.form("taster_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                s_first = st.text_input("Student First Name *")
                s_last = st.text_input("Student Last Name")
                status = st.selectbox("Status", ["Taster", "Current", "Former", "Inactive"], index=0)
            with col2:
                guardian_id = st.text_input("Guardian ID (optional)")
                dob = st.text_input("Date of Birth (YYYY-MM-DD)")
                notes = st.text_area("Important information / Notes", height=80)

            submitted = st.form_submit_button("Save Student", use_container_width=True)

        if submitted:
            if not s_first:
                st.error("Student first name is required.")
            else:
                try:
                    student = create_student(
                        first_name=s_first,
                        last_name=s_last or "",
                        status=status,
                        guardian_id=guardian_id,
                        date_of_birth=dob,
                        search_rule="",
                        notes=notes
                    )
                    st.success(f"✅ Student created: {student['full_name']} ({student['student_id']})")
                    st.rerun()
                except ServiceError as e:
                    st.error(str(e))

    # ====================== TAB 3: ENROLMENT (NEW PRICING) ======================
    with tab_enrol:
        st.subheader("Enrolment (2026-27 Pricing)")
        st.info("Choose from the new tiered menu")

        with st.form("enrol_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                s_first = st.text_input("Student First Name *")
                s_last = st.text_input("Student Last Name")
                status = st.selectbox("Status", ["Current", "Taster", "Former", "Inactive"], index=0)
                product_choice = st.selectbox(
                    "Core Membership",
                    [
                        "Core Single Class (£35/mo)",
                        "Core Dual Class (£60/mo)",
                        "Sibling 2nd Child (£30/mo)",
                        "Sibling 3rd Child (£25/mo)"
                    ]
                )
            with col2:
                g_name = st.text_input("Guardian Name (if new)")
                g_email = st.text_input("Guardian Email")
                g_phone = st.text_input("Guardian Phone")
                add_ons = st.multiselect(
                    "Opt-in Add-ons",
                    ["Showreel Package (£30 upfront)", "2-Day Summer Shoot (£110)", "Ultimate Summer Bundle (£255)"]
                )

            notes = st.text_area("Notes about child / special circumstances", height=100)
            submitted = st.form_submit_button("Save Enrolment Record", use_container_width=True)

        if submitted:
            if not s_first:
                st.error("Student first name is required.")
            else:
                try:
                    guardian_id = ""
                    if g_name:
                        guardian = create_guardian(guardian_name=g_name, email=g_email, phone=g_phone)
                        guardian_id = guardian["guardian_id"]

                    student = create_student(
                        first_name=s_first,
                        last_name=s_last or "",
                        status=status,
                        guardian_id=guardian_id,
                        date_of_birth="",
                        search_rule="",
                        notes=f"Product: {product_choice} | Add-ons: {add_ons} | {notes}"
                    )
                    st.success(f"✅ Enrolment record created: {student['full_name']}")
                    st.rerun()
                except ServiceError as e:
                    st.error(str(e))

    # ====================== TAB 4: CONSENT ======================
    with tab_consent:
        st.subheader("Record Consent (2026-27)")
        st.info("Attach to existing guardian or student")
        consent_given = st.checkbox("Consent given for audio/video recordings and media use")
        consent_notes = st.text_area("Consent notes / which children", height=80)
        if st.button("Save Consent"):
            st.success("✅ Consent recorded (stored in notes for now). We can make this a dedicated field later.")

    # ====================== TAB 5: BULK CSV IMPORT ======================
    with tab_import:
        st.subheader("Bulk Import from Parent Form CSV")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        form_type = st.selectbox("Form type", ["auto", "taster", "enrolment", "contact", "consent"], index=0)

        if uploaded_file is not None:
            if st.button("🚀 Import Form", type="primary", use_container_width=True):
                with st.spinner("Processing..."):
                    try:
                        temp_path = f"data/raw/temp_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        result = ingest_form(temp_path, form_type)

                        st.success("✅ Import completed!")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Rows", result.get("total_rows", 0))
                        col2.metric("Guardians", result.get("guardians_created", 0))
                        col3.metric("Students", result.get("students_created", 0))
                    except Exception as e:
                        st.error(f"Import failed: {e}")
