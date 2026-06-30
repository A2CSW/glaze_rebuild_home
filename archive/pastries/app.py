import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd

from core.data_loader import (
    load_all, save_students, save_contacts, 
    save_medical, save_memberships
)
from config.settings import MEMBERSHIP_PRICES, SIBLING_PRICES

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(page_title="Glaze", layout="wide")

# =============================================
# LOAD & PRE-PROCESS DATA
# =============================================
students, attendance, payments, medical, contacts, memberships, addons, enrolments = load_all()
# Current students for matching
current = students[students["status"] == "Current"].copy()

if "search_rule" not in current.columns:
    current["search_rule"] = ""
else:
    current["search_rule"] = current["search_rule"].fillna("")

# Data cleanup
payments = payments.dropna(subset=["student_id"]).copy()
students["full_name"] = students["full_name"].astype(str).str.strip()

months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"]

# Process payments
payments[months] = payments[months].apply(pd.to_numeric, errors="coerce").fillna(0)
payments["total_paid"] = payments[months].sum(axis=1)

# Create useful merged views
student_payment_view = students.merge(
    payments[["student_id"] + months + ["total_paid"]],
    on="student_id", how="left"
).fillna({"total_paid": 0})

tracker = students.copy()
for m in months:
    if m not in tracker.columns:
        tracker[m] = 0
tracker[months] = tracker[months].apply(pd.to_numeric, errors="coerce").fillna(0)
tracker["total_paid"] = tracker[months].sum(axis=1)
tracker["status"] = tracker.get("status", pd.Series("Current", index=tracker.index)).fillna("Current")

# =============================================
# UI - TABS
# =============================================
st.title("GLAZE")
st.caption("Guiding Light Admin Zone Ecosystem")

tab1, tab2, tab3 = st.tabs([
    "👩‍🎓 Students", 
    "📅 Classes", 
    "💰 Payments", 
])

# =============================================
# TAB 1: STUDENTS
# =============================================
with tab1:

    st.subheader("Students")


    # ====================== ADD NEW STUDENT ======================

    if "add_student_mode" not in st.session_state:
        st.session_state.add_student_mode = False


    if st.button(
        "➕ Add New Student",
        type="primary",
        use_container_width=True
    ):
        st.session_state.add_student_mode = True


    if st.session_state.add_student_mode:

        st.divider()
        st.subheader("Add New Student")


        col1, col2 = st.columns(2)


        with col1:

            st.write("**Student Information**")

            new_full_name = st.text_input(
                "Full Name",
                key="new_full_name"
            )

            new_dob = st.text_input(
                "Date of Birth",
                key="new_dob"
            )

            new_status = st.selectbox(
                "Status",
                ["Current", "Taster", "Former"],
                key="new_status"
            )


        with col2:

            st.write("**Medical & Permissions**")

            med_notes = st.text_area(
                "Medical Notes",
                key="new_med_notes"
            )

            med_consent = st.text_input(
                "Media Consent",
                key="new_media_consent"
            )


        st.divider()


        # ====================== CONTACTS ======================

        st.subheader("Contacts")

        colA, colB = st.columns(2)


        with colA:

            st.write("**Guardian 1**")

            g1_name = st.text_input(
                "Guardian 1 Name",
                key="new_g1_name"
            )

            g1_email = st.text_input(
                "Guardian 1 Email",
                key="new_g1_email"
            )

            g1_mobile = st.text_input(
                "Guardian 1 Mobile",
                key="new_g1_mobile"
            )


        with colB:

            st.write("**Guardian 2**")

            g2_name = st.text_input(
                "Guardian 2 Name",
                key="new_g2_name"
            )

            g2_email = st.text_input(
                "Guardian 2 Email",
                key="new_g2_email"
            )

            g2_mobile = st.text_input(
                "Guardian 2 Mobile",
                key="new_g2_mobile"
            )

            e_name = st.text_input(
                "Emergency Name",
                key="new_emergency_name"
            )

            e_mobile = st.text_input(
                "Emergency Mobile",
                key="new_emergency_mobile"
            )


        st.divider()


        # ====================== MEMBERSHIP ======================

        st.subheader("Membership")


        new_mem_type = st.selectbox(
            "Membership Type",
            list(MEMBERSHIP_PRICES.keys()),
            key="new_membership_type"
        )


        new_sibling = st.selectbox(
            "Sibling Position",
            [
                "1st Child",
                "2nd Child",
                "3rd+ Child"
            ],
            key="new_sibling_position"
        )


        monthly_fee = (
            MEMBERSHIP_PRICES.get(new_mem_type,0)
            if new_sibling == "1st Child"
            else SIBLING_PRICES.get(new_sibling,0)
        )


        st.info(f"Monthly Fee: £{monthly_fee}")


        # ====================== SAVE NEW STUDENT ======================

        if st.button(
            "💾 Create Student",
            type="primary",
            use_container_width=True
        ):


            # Generate next ID safely

            existing_numbers = (
                students["student_id"]
                .astype(str)
                .str.extract(r"(\d+)")
                [0]
                .dropna()
                .astype(int)
            )


            next_number = (
                existing_numbers.max() + 1
                if not existing_numbers.empty
                else 1
            )


            new_id = f"STU{next_number:04d}"


            # Students

            students.loc[len(students)] = {
                "student_id": new_id,
                "full_name": new_full_name,
                "dob": new_dob,
                "status": new_status
            }


            # Medical

            medical.loc[len(medical)] = {
                "student_id": new_id,
                "medical_notes": med_notes,
                "media_consent": med_consent
            }


            # Contacts

            contacts.loc[len(contacts)] = {

                "student_id": new_id,

                "guardian_1_name": g1_name,
                "guardian_1_email": g1_email,
                "guardian_1_mobile": g1_mobile,

                "guardian_2_name": g2_name,
                "guardian_2_email": g2_email,
                "guardian_2_mobile": g2_mobile,

                "emergency_name": e_name,
                "emergency_mobile": e_mobile
            }


            # Memberships

            memberships.loc[len(memberships)] = {

                "student_id": new_id,
                "membership_type": new_mem_type,
                "sibling_position": new_sibling
            }


            save_students(students)
            save_medical(medical)
            save_contacts(contacts)
            save_memberships(memberships)


            st.success(
                f"✅ Created {new_full_name} ({new_id})"
            )

            st.session_state.add_student_mode = False

            st.rerun()

    # --------------------- Individual Student Search ---------------------
    selected_student = st.selectbox(
        "Search & open student",
        options=students["full_name"].tolist(),
        index=None,
        placeholder="Type to search and select a student..."
    )

    if selected_student:
        student = students[students["full_name"] == selected_student].iloc[0]
        student_id = student["student_id"]

        st.divider()
        st.subheader(student["full_name"])

        # ==================== READ-ONLY DISPLAY ====================
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Student Details**")
            st.write("Name:", student["full_name"])
            st.write("Date of Birth:", student.get("dob", "—"))
            st.write("Status:", student.get("status", "Current"))

            # === CLASSES ATTENDED (from attendance_tracker) ===
            st.write("**Classes Attended**")
            student_classes = attendance[attendance["student_id"] == student_id]
            if not student_classes.empty:
                class_list = student_classes["classes"].dropna().unique().tolist()
                for cls in class_list:
                    st.write(f"• {cls}")
            else:
                st.write("No class records found")

        with col2:
            st.write("**Medical**")
            med_record = medical[medical["student_id"] == student_id]
            if not med_record.empty:
                m = med_record.iloc[0]
                st.write("Notes:", m.get("medical_notes", "—"))
                st.write("Media Consent:", m.get("media_consent", "—"))

            st.write("**Membership**")
            mem_record = memberships[memberships["student_id"] == student_id]
            if not mem_record.empty:
                mem = mem_record.iloc[0]
                st.write("Type:", mem.get("membership_type", "—"))
                st.write("Sibling Position:", mem.get("sibling_position", "—"))

        st.divider()

# ====================== EDIT MODE ======================
        edit_mode = st.toggle("✏️ Edit Student", value=False)

        if edit_mode:
            st.divider()
            st.subheader("Edit Student")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Student Information**")
                new_full_name = st.text_input("Full Name", value=student.get("full_name", ""))
                new_dob = st.text_input("Date of Birth", value=student.get("dob", ""))
                new_status = st.selectbox(
                    "Status",
                    ["Current", "Taster", "Former"],
                    index=["Current", "Taster", "Former"].index(student.get("status", "Current"))
                )

                # Classes Attended (read-only)
                st.write("**Classes Attended**")
                student_classes = attendance[attendance["student_id"] == student_id]
                if not student_classes.empty:
                    class_list = student_classes["classes"].dropna().unique().tolist()
                    st.write("• " + "\n• ".join(class_list))
                else:
                    st.write("No class records found")

            with col2:
                st.write("**Medical & Permissions**")
                med_record = medical[medical["student_id"] == student_id]
                med_notes = st.text_area(
                    "Medical Notes", 
                    value=med_record.iloc[0]["medical_notes"] if not med_record.empty else ""
                )
                med_consent = st.text_input(
                    "Media Consent", 
                    value=med_record.iloc[0].get("media_consent", "") if not med_record.empty else ""
                )

            st.divider()

            # ====================== CONTACTS ======================
            st.subheader("Contacts")
            contact_record = contacts[contacts["student_id"] == student_id]
            c = contact_record.iloc[0] if not contact_record.empty else {}

            colA, colB = st.columns(2)
            with colA:
                st.write("**Guardian 1**")

                g1_name = st.text_input(
                    "Guardian 1 Name",
                    value=c.get("guardian_1_name", "")
                )

                g1_email = st.text_input(
                    "Guardian 1 Email",
                    value=c.get("guardian_1_email", "")
                )

                g1_mobile = st.text_input(
                    "Guardian 1 Mobile",
                    value=str(c.get("guardian_1_mobile", "")).replace(".0", "")
                )

            with colB:
                st.write("**Guardian 2**")

                g2_name = st.text_input(
                    "Guardian 2 Name",
                    value=c.get("guardian_2_name", "")
                )

                g2_email = st.text_input(
                    "Guardian 2 Email",
                    value=c.get("guardian_2_email", "")
                )

                g2_mobile = st.text_input(
                    "Guardian 2 Mobile",
                    value=str(c.get("guardian_2_mobile", "")).replace(".0", "")
                )

                st.write("**Emergency Contact**")

                e1_name = st.text_input(
                    "Emergency Name",
                    value=c.get("emergency_name", "")
                )

                e1_mobile = st.text_input(
                    "Emergency Mobile",
                    value=str(c.get("emergency_mobile", "")).replace(".0", "")
                )
	
            st.divider()

            # ====================== MEMBERSHIP ======================
            st.subheader("Membership")
            mem_record = memberships[memberships["student_id"] == student_id]
            if not mem_record.empty:
                mem = mem_record.iloc[0]
                mem_type = st.selectbox("Membership Type", list(MEMBERSHIP_PRICES.keys()),
                                        index=list(MEMBERSHIP_PRICES.keys()).index(mem.get("membership_type", list(MEMBERSHIP_PRICES.keys())[0])))
                sibling_pos = st.selectbox("Sibling Position", ["1st Child", "2nd Child", "3rd+ Child"],
                                           index=["1st Child", "2nd Child", "3rd+ Child"].index(mem.get("sibling_position", "1st Child")))
                monthly_fee = MEMBERSHIP_PRICES.get(mem_type, 0) if sibling_pos == "1st Child" else SIBLING_PRICES.get(sibling_pos, 0)
                st.info(f"**Monthly Fee: £{monthly_fee}**")

            # ====================== SAVE BUTTON ======================
            if st.button("💾 Save All Student Changes", type="primary", use_container_width=True):
                # Update Students table
                students.loc[students["student_id"] == student_id, ["full_name", "dob", "status"]] = [new_full_name, new_dob, new_status]

                # Update Medical (safe)
                if not med_record.empty:
                    idx = med_record.index[0]
                    medical.loc[idx, ["medical_notes", "media_consent"]] = [med_notes, med_consent]

# Update Contacts - SAFEST METHOD
                if not contact_record.empty:
                    idx = contact_record.index[0]

                    # Force string types to prevent dtype errors
                    contacts["guardian_1_name"] = contacts["guardian_1_name"].astype(str)
                    contacts["guardian_1_email"] = contacts["guardian_1_email"].astype(str)
                    contacts["guardian_1_mobile"] = contacts["guardian_1_mobile"].astype(str)

                    contacts["guardian_2_name"] = contacts["guardian_2_name"].astype(str)
                    contacts["guardian_2_email"] = contacts["guardian_2_email"].astype(str)
                    contacts["guardian_2_mobile"] = contacts["guardian_2_mobile"].astype(str)

                    contacts["emergency_name"] = contacts["emergency_name"].astype(str)
                    contacts["emergency_mobile"] = contacts["emergency_mobile"].astype(str)


                    # Save Guardian 1 + Guardian 2
                    contacts.loc[idx, [
                        "guardian_1_name",
                        "guardian_1_email",
                        "guardian_1_mobile",
                        "guardian_2_name",
                        "guardian_2_email",
                        "guardian_2_mobile",
                        "emergency_name",
                        "emergency_mobile"
                    ]] = [
                        g1_name,
                        g1_email,
                        g1_mobile,
                        g2_name,
                        g2_email,
                        g2_mobile,
                        e1_name,
                        e1_mobile
                    ]

                # Update Membership
                if not mem_record.empty:
                    idx = mem_record.index[0]
                    memberships.loc[idx, ["membership_type", "sibling_position"]] = [mem_type, sibling_pos]

                # Save everything
                save_students(students)
                save_medical(medical)
                save_contacts(contacts)
                save_memberships(memberships)

                st.success(f"✅ All changes saved for **{new_full_name}**!")
                st.rerun()

    # =============================================
    # ALL STUDENTS LIST / STATUS MANAGEMENT
    # =============================================
    st.divider()
    st.subheader("All Students")

    colA, colB = st.columns([4, 1])

    with colA:

        st.caption("Filter students by status")

        status_filter = st.selectbox(
            "Status Filter",
            ["All", "Taster", "Current", "Former"],
            key="student_status_filter"
        )

        student_list = students.copy()

        # Add classes display
        def get_classes(student_id):
            records = attendance[
                attendance["student_id"] == student_id
            ]

            if not records.empty:
                return ", ".join(
                    records["classes"]
                    .dropna()
                    .unique()
                    .tolist()
                )

            return ""

        student_list["classes"] = (
            student_list["student_id"]
            .apply(get_classes)
        )


        if status_filter != "All":
            student_list = student_list[
                student_list["status"] == status_filter
            ]


        student_list = (
            student_list
            .sort_values("full_name")
            .reset_index(drop=True)
        )


        # Editable table
        edited_students = st.data_editor(
            student_list[
                [
                    "full_name",
                    "status",
                    "classes"
                ]
            ],
            use_container_width=True,
            hide_index=True,
            disabled=[
                "full_name",
                "classes"
            ],
            column_config={
                "full_name": st.column_config.TextColumn(
                    "Student Name"
                ),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=[
                        "Taster",
                        "Current",
                        "Former"
                    ]
                ),
                "classes": st.column_config.TextColumn(
                    "Classes"
                )
            },
            key="student_status_editor"
        )


    with colB:

        st.markdown("## Student Count")

        taster_count = (
            students["status"]
            .eq("Taster")
            .sum()
        )

        current_count = (
            students["status"]
            .eq("Current")
            .sum()
        )

        former_count = (
            students["status"]
            .eq("Former")
            .sum()
        )


        st.metric(
            "Tasters",
            f"+{taster_count}"
        )

        st.metric(
            "Current",
            f"+{current_count}"
        )

        st.metric(
            "Former",
            f"+{former_count}"
        )


        st.divider()


        if st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True
        ):

            for index, row in edited_students.iterrows():

                student_name = row["full_name"]
                new_status = row["status"]

                students.loc[
                    students["full_name"] == student_name,
                    "status"
                ] = new_status


            save_students(students)

            st.success(
                "✅ Student statuses saved"
            )

            st.rerun()

# =============================================
# TAB 2: CLASSES
# =============================================
with tab2:
    st.subheader("📅 Classes Overview")
    st.caption("Students by actual classes attended")

    # Prepare data
    class_view = students.copy()

    if not attendance.empty and "classes" in attendance.columns:
        att_summary = (
            attendance.groupby("student_id")["classes"]
            .agg(lambda x: ", ".join(sorted(x.dropna().unique())))
            .reset_index(name="classes")
        )
        class_view = class_view.merge(att_summary, on="student_id", how="left")
    else:
        class_view["classes"] = "No class data"

    # Calculate Age
    if "dob" in class_view.columns:
        class_view["dob"] = pd.to_datetime(class_view["dob"], errors="coerce")
        class_view["Age"] = (pd.Timestamp.today() - class_view["dob"]).dt.days // 365

    # Unique classes for dropdown
    all_classes = []
    if "classes" in class_view.columns:
        all_classes = sorted(set(
            cls.strip() 
            for cell in class_view["classes"].dropna() 
            for cls in str(cell).split(",") 
            if cls.strip()
        ))

    # ==================== FILTERS ====================
    st.write("**Filters**")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        status_filter = st.multiselect("Status", ["Current", "Taster", "Former"], default=["Current"])
    with col2:
        selected_classes = st.multiselect("Filter by Class", options=all_classes, placeholder="Select classes")
    with col3:
        cohort_filter = st.selectbox("Filter by Cohort", 
                                   ["All", "Littlies", "Middlies", "Oldies"], index=0)
    with col4:
        membership_filter = st.selectbox("Membership Type", 
                                       ["All", "Member", "Enrolled"], index=0)
        age_min, age_max = st.slider("Age Range", 3, 18, (5, 15))

    # Apply filters
    filtered = class_view.copy()

    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    if selected_classes:
        mask = filtered["classes"].astype(str).apply(
            lambda x: any(cls in x for cls in selected_classes)
        )
        filtered = filtered[mask]
    if cohort_filter != "All":
        filtered = filtered[filtered["cohort"].str.contains(cohort_filter, case=False, na=False)]
    if membership_filter != "All":
        filtered = filtered[filtered["membership_type"].str.contains(membership_filter, case=False, na=False)]
    if "Age" in filtered.columns:
        filtered = filtered[(filtered["Age"] >= age_min) & (filtered["Age"] <= age_max)]

    filtered = filtered.sort_values(by="full_name")

    # ==================== DISPLAY ====================
    display_cols = ["full_name", "status", "Age", "cohort", "membership_type", "classes"]

    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "full_name": st.column_config.TextColumn("Student Name", width="large"),
            "status": st.column_config.TextColumn("Status"),
            "Age": st.column_config.NumberColumn("Age"),
            "cohort": st.column_config.TextColumn("Cohort"),
            "membership_type": st.column_config.TextColumn("Membership"),
            "classes": st.column_config.TextColumn("Classes Attended", width="medium"),
        }
    )

    st.caption(f"**Showing {len(filtered)} students**")

    # ==================== EXPORT BUTTONS ====================
    st.divider()
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        if st.button("📥 Export Current Filtered List to CSV", use_container_width=True):
            csv = filtered[display_cols].to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV Now",
                data=csv,
                file_name=f"glaze_classes_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with col_exp2:
        if st.button("📥 Export ALL Students to CSV", use_container_width=True):
            all_csv = class_view[display_cols].to_csv(index=False)
            st.download_button(
                label="⬇️ Download Full List CSV",
                data=all_csv,
                file_name=f"glaze_all_students_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# =============================================
# TAB 3: BANK IMPORT & RULE EDITOR
# =============================================
with tab3:
    st.subheader("🏦 Bank Statement Import & Rule Editor")
    st.caption("Define search rules for students + upload & match bank statements")

    # =============================================
    # SECTION 1: SEARCH RULES EDITOR
    # =============================================
    st.subheader("1. Search Rules Editor")

    if "show_search_rules" not in st.session_state:
        st.session_state["show_search_rules"] = False

    if st.button(
        "🔍 Show Search Rules" if not st.session_state["show_search_rules"] else "🔍 Hide Search Rules",
        type="primary",
        use_container_width=True
    ):
        st.session_state["show_search_rules"] = (
            not st.session_state["show_search_rules"]
        )

    if st.session_state["show_search_rules"]:

        st.caption("Previously saved rules will appear below. Edit and click Save.")

        rule_df = current[
            [
                "full_name",
                "search_rule"
            ]
        ].copy()

        edited = st.data_editor(
            rule_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "full_name": st.column_config.TextColumn(
                    "Student Name",
                    disabled=True
                ),
                "search_rule": st.column_config.TextColumn(
                    "🔑 Search Rule / Keyword"
                ),
            },
            key="search_rules_editor_v2"
        )

        if st.button(
            "💾 Save Search Rules",
            type="primary",
            use_container_width=True
        ):
            students.loc[
                students["status"] == "Current",
                "search_rule"
            ] = edited["search_rule"].fillna("")

            save_students(students)

            st.success("✅ Search rules saved successfully!")
            st.rerun()

    st.divider()

    # =============================================
    # SECTION 2: BANK STATEMENT UPLOADER
    # =============================================
    st.subheader("2. Bank Statement Uploader")
    uploaded_file = st.file_uploader("Upload Bank File", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(('.xls', '.xlsx')):
                bank_df = pd.read_excel(uploaded_file)
            else:
                bank_df = pd.read_csv(uploaded_file)

            st.success(f"✅ Loaded {len(bank_df)} transactions")

            st.subheader("Preview")
            st.dataframe(bank_df.head(10), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

    st.divider()

    # =============================================
    # SECTION 3: RUN MATCHING
    # =============================================
    st.subheader("3. Run Matching")

    if uploaded_file is not None and st.button("🚀 Run Matching Now", type="primary"):
        with st.spinner("Matching..."):
            from thefuzz import process, fuzz

            results = []
            for _, row in bank_df.iterrows():
                desc = str(row.get("Transaction Description", "")).upper().strip()

                best_match = "No match"
                confidence = 0
                rule_used = ""

                for _, student in current.iterrows():
                    rule = str(student.get("search_rule", "")).strip().upper()
                    if rule and rule in desc:
                        best_match = student["full_name"]
                        confidence = 95
                        rule_used = rule
                        break

                if confidence == 0:
                    best = process.extractOne(desc, current["full_name"].tolist(), scorer=fuzz.token_sort_ratio)
                    if best and best[1] >= 60:
                        best_match = best[0]
                        confidence = best[1]

                status = "High" if confidence >= 80 else "Review" if confidence >= 50 else "Unmatched"

                results.append({
                    "Date": row.get("Transaction Date"),
                    "Description": str(row.get("Transaction Description", ""))[:80],
                    "Amount": row.get("Credit Amount") or 0,
                    "Best Match": best_match,
                    "Confidence": confidence,
                    "Status": status,
                    "Rule Used": rule_used
                })

            match_df = pd.DataFrame(results)

            c1, c2, c3 = st.columns(3)
            c1.metric("✅ High Confidence", len(match_df[match_df["Confidence"] >= 80]))
            c2.metric("⚠️ Needs Review", len(match_df[(match_df["Confidence"] >= 50) & (match_df["Confidence"] < 80)]))
            c3.metric("❌ Unmatched", len(match_df[match_df["Confidence"] < 50]))

            st.dataframe(match_df.sort_values("Confidence", ascending=False), use_container_width=True, hide_index=True)

# =============================================
# SECTION 4: REVIEW MATCHES
# =============================================

with tab3:

    st.divider()
    st.subheader("4. Review Matches")


    if "match_df" not in st.session_state:

        st.warning("Please run matching first.")


    else:

        # =============================================
        # PREPARE REVIEW DATA
        # =============================================

        st.caption(
            "Review suggested matches below. Tick Approve when the payment match is correct."
        )

        review_df = st.session_state["match_df"].copy()



        # =============================================
        # ADD STUDENT SEARCH RULE KEYWORD
        # =============================================

        current_lookup = current[
            [
                "full_name",
                "search_rule"
            ]
        ].copy()


        current_lookup = current_lookup.rename(
            columns={
                "full_name": "Best Match",
                "search_rule": "Student Keyword"
            }
        )


        review_df = review_df.merge(
            current_lookup,
            on="Best Match",
            how="left"
        )



        # =============================================
        # FORMAT DISPLAY COLUMNS
        # =============================================

        review_df = review_df.rename(
            columns={
                "Best Match": "Student Name",
                "Description": "Transaction Description",
                "Amount": "Fee"
            }
        )


        # Default approve high-confidence matches

        review_df["Approve"] = (
            review_df["Confidence"] >= 80
        )


        # Highest confidence first

        review_df = (
            review_df
            .sort_values(
                by="Confidence",
                ascending=False
            )
            .reset_index(drop=True)
        )



        # =============================================
        # MATCH APPROVAL TABLE
        # =============================================

        st.subheader("Match Approval List")


        review_editor = st.data_editor(

            review_df[
                [
                    "Student Name",
                    "Student Keyword",
                    "Transaction Description",
                    "Fee",
                    "Confidence",
                    "Approve"
                ]
            ],

            use_container_width=True,
            hide_index=True,


            disabled=[
                "Student Name",
                "Student Keyword",
                "Transaction Description",
                "Fee",
                "Confidence"
            ],


            column_config={

                "Student Name":
                    st.column_config.TextColumn(
                        "Student"
                    ),


                "Student Keyword":
                    st.column_config.TextColumn(
                        "Keyword"
                    ),


                "Transaction Description":
                    st.column_config.TextColumn(
                        "Bank Description"
                    ),


                "Fee":
                    st.column_config.NumberColumn(
                        "Fee (£)"
                    ),


                "Confidence":
                    st.column_config.NumberColumn(
                        "Confidence %"
                    ),


                "Approve":
                    st.column_config.CheckboxColumn(
                        "Approve"
                    )
            },


            key="match_review_editor"
        )



        # =============================================
        # REVIEW SUMMARY
        # =============================================

        approved_count = review_editor["Approve"].sum()


        st.info(
            f"✅ {approved_count} matches currently approved for saving"
        )



    # =============================================
    # SECTION 5: EXPORT MATCHING REPORT
    # =============================================

    st.divider()

    st.subheader("5. Export Matching Report")


    st.caption(
        "Download a copy of the current bank matching results for review or records."
    )


    if "match_df" in st.session_state:


        st.download_button(
            "⬇️ Download Report",

            st.session_state["match_df"].to_csv(
                index=False
            ),

            f"bank_matching_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",

            mime="text/csv"
        )


    else:


        st.info(
            "Run matching first to generate a report."
        )
