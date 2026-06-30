from __future__ import annotations
import streamlit as st
from services.form_ingestion_service import ingest_form

def render_import_forms_page() -> None:
    st.header("📥 Import Parent Forms")
    st.caption("Upload CSV files from Enquiry, Taster, Enrolment or Consent forms")

    with st.expander("How to use this page", expanded=False):
        st.markdown("""
        1. Export your form responses as CSV from Google Forms / Typeform / etc.
        2. Upload the CSV below.
        3. Select the correct form type (or let it auto-detect).
        4. Click **Import**.
        5. The file will be processed and archived.
        """)

    uploaded_file = st.file_uploader(
        "Upload form CSV",
        type=["csv"],
        help="CSV exported from your parent forms"
    )

    form_type = st.selectbox(
        "Form type (or leave as Auto-detect)",
        ["auto", "taster", "enrolment", "contact", "consent"],
        index=0
    )

    if uploaded_file is not None:
        if st.button("🚀 Import Form", type="primary", use_container_width=True):
            with st.spinner("Processing form..."):
                try:
                    # Save uploaded file temporarily
                    temp_path = f"data/raw/temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Run ingestion
                    result = ingest_form(temp_path, form_type)

                    st.success("✅ Import completed!")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Rows processed", result.get("total_rows", 0))
                    col2.metric("Guardians created", result.get("guardians_created", 0))
                    col3.metric("Students created", result.get("students_created", 0))

                    if result.get("errors"):
                        st.warning("Some rows had issues:")
                        for err in result["errors"]:
                            st.error(err)
                    else:
                        st.info("All rows processed successfully.")

                    st.caption(f"File archived as: {result.get('archived_as', 'N/A')}")

                except Exception as e:
                    st.error(f"Import failed: {e}")
