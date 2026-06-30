from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.product_service import create_product, update_product
from services.query_service import get_products_view, get_programmes_view
def render_products_page() -> None:
    st.header("Products")
    programmes = get_programmes_view()
    programme_options = [""]
    programme_labels = {"": "(No programme linked)"}
    if not programmes.empty:
        for _, row in programmes.iterrows():
            programme_id = str(row["programme_id"]).strip()
            programme_name = str(row["name"]).strip()
            programme_options.append(programme_id)
            programme_labels[programme_id] = f"{programme_name} ({programme_id})"
    with st.expander("Add Product", expanded=False):
        with st.form("add_product_form", clear_on_submit=True):
            name = st.text_input("Product name")
            programme_id = st.selectbox(
                "Programme",
                options=programme_options,
                format_func=lambda x: programme_labels.get(x, x),
            )
            status = st.selectbox("Status", ["Active", "Inactive", "Draft"], index=0)
            submitted = st.form_submit_button("Save Product")
        if submitted:
            try:
                record = create_product(name=name, programme_id=programme_id, status=status)
                st.success(f"Product created: {record['name']} ({record['product_id']})")
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    df = get_products_view()
    st.write(f"Rows: {len(df)}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if df.empty:
        return
    st.subheader("Edit Existing Product")
    product_options = df["product_id"].astype(str).tolist()
    labels = {
        str(row["product_id"]): f"{row['name']} ({row['product_id']})"
        for _, row in df.iterrows()
    }
    selected_product_id = st.selectbox(
        "Select product",
        options=product_options,
        format_func=lambda x: labels.get(x, x),
    )
    row = df[df["product_id"].astype(str) == selected_product_id].iloc[0]
    with st.form("edit_product_form"):
        name = st.text_input("Product name", value=str(row.get("name", "")))
        current_programme_id = str(row.get("programme_id", ""))
        programme_index = programme_options.index(current_programme_id) if current_programme_id in programme_options else 0
        programme_id = st.selectbox(
            "Programme",
            options=programme_options,
            index=programme_index,
            format_func=lambda x: programme_labels.get(x, x),
        )
        statuses = ["Active", "Inactive", "Draft"]
        current_status = str(row.get("status", "Active"))
        status_index = statuses.index(current_status) if current_status in statuses else 0
        status = st.selectbox("Status", statuses, index=status_index)
        submitted = st.form_submit_button("Update Product")
    if submitted:
        try:
            record = update_product(
                product_id=selected_product_id,
                name=name,
                programme_id=programme_id,
                status=status,
            )
            st.success(f"Product updated: {record['name']} ({record['product_id']})")
            st.rerun()
        except ServiceError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
