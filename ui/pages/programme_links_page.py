from __future__ import annotations
import streamlit as st
from core.exceptions import ServiceError
from services.link_service import link_programme_to_class, link_programme_to_product
from services.query_service import (
    get_classes_view,
    get_products_view,
    get_programme_classes_view,
    get_programme_products_view,
    get_programmes_view,
)
def render_programme_links_page() -> None:
    st.header("Programme Links")
    programmes = get_programmes_view()
    products = get_products_view()
    classes = get_classes_view()
    if programmes.empty:
        st.warning("Create at least one programme first.")
        return
    programme_options = []
    programme_labels: dict[str, str] = {}
    for _, row in programmes.iterrows():
        programme_id = str(row["programme_id"]).strip()
        programme_name = str(row["name"]).strip()
        programme_options.append(programme_id)
        programme_labels[programme_id] = f"{programme_name} ({programme_id})"
    st.subheader("Link Programme to Product")
    if products.empty:
        st.info("No products available yet.")
    else:
        product_options = []
        product_labels: dict[str, str] = {}
        for _, row in products.iterrows():
            product_id = str(row["product_id"]).strip()
            product_name = str(row["name"]).strip()
            product_options.append(product_id)
            product_labels[product_id] = f"{product_name} ({product_id})"
        with st.form("link_programme_product_form", clear_on_submit=True):
            programme_id = st.selectbox(
                "Programme",
                options=programme_options,
                format_func=lambda x: programme_labels.get(x, x),
                key="programme_product_programme",
            )
            product_id = st.selectbox(
                "Product",
                options=product_options,
                format_func=lambda x: product_labels.get(x, x),
                key="programme_product_product",
            )
            submitted = st.form_submit_button("Create Programme -> Product Link")
        if submitted:
            try:
                record = link_programme_to_product(
                    programme_id=programme_id,
                    product_id=product_id,
                )
                st.success(
                    f"Link created: {record['programme_id']} -> {record['product_id']}"
                )
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    st.subheader("Link Programme to Class")
    if classes.empty:
        st.info("No classes available yet.")
    else:
        class_options = []
        class_labels: dict[str, str] = {}
        for _, row in classes.iterrows():
            class_id = str(row["class_id"]).strip()
            class_name = str(row["name"]).strip()
            class_labels[class_id] = f"{class_name} ({class_id})"
            class_options.append(class_id)
        with st.form("link_programme_class_form", clear_on_submit=True):
            programme_id = st.selectbox(
                "Programme",
                options=programme_options,
                format_func=lambda x: programme_labels.get(x, x),
                key="programme_class_programme",
            )
            class_id = st.selectbox(
                "Class",
                options=class_options,
                format_func=lambda x: class_labels.get(x, x),
                key="programme_class_class",
            )
            submitted = st.form_submit_button("Create Programme -> Class Link")
        if submitted:
            try:
                record = link_programme_to_class(
                    programme_id=programme_id,
                    class_id=class_id,
                )
                st.success(
                    f"Link created: {record['programme_id']} -> {record['class_id']}"
                )
                st.rerun()
            except ServiceError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
    st.subheader("Existing Programme -> Product Links")
    programme_product_links = get_programme_products_view()
    st.write(f"Rows: {len(programme_product_links)}")
    st.dataframe(programme_product_links, use_container_width=True, hide_index=True)
    st.subheader("Existing Programme -> Class Links")
    programme_class_links = get_programme_classes_view()
    st.write(f"Rows: {len(programme_class_links)}")
    st.dataframe(programme_class_links, use_container_width=True, hide_index=True)
