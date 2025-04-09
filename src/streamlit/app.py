"""Streamlit application for Satellite Data Downloader.

This module provides the main function to run the Streamlit app,
including UI components and search functionality.
"""

from datetime import datetime, timezone

import streamlit as st
from src.streamlit.utils.download_links import display_download_links
from src.streamlit.utils.geojson_utils import extract_bbox
from src.streamlit.utils.stac_search import (
    search_sar_items,
    search_truecolor_items,
)

st.set_page_config(
    page_title="Satellite Data Downloader",
    page_icon="src/streamlit/assets/MA-logo.png",
    layout="wide",
)

def main() -> None:
    """Main function to run the Streamlit app."""
    # -- LOGO + TITLE
    # Use st.image() so Streamlit can handle the file
    st.image("src/streamlit/assets/MA-logo.png", width=250)
    st.title("Satellite Data Downloader")
    st.write("Easily search and download satellite imagery files.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # -- INSTRUCTIONS
    st.subheader("Instructions")
    st.write(
        """
        1. **Upload** a GeoJSON file containing your desired Area of Interest (AOI).  
        2. **Adjust** the search settings (e.g., product type, dates, cloud cover).  
        3. **Click Search** to find matching satellite imagery.  
        4. **Download** files from the results list.
        """
    )

    st.markdown("### Search Criteria")
    st.write("Upload a polygon GeoJSON (or .json) to extract bounding box:")

    # -- SEARCH FORM
    with st.form("search_form"):
        uploaded_file = st.file_uploader(
            label="Drag and drop file here",
            type=["geojson", "json"],
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([2, 2])
        with col1:
            product_type = st.selectbox(
                "Product Type", ["truecolor", "sar"], index=0
            )
        with col2:
            cloud_cover = st.slider("Max Cloud Cover (%)", 1, 100, 10)

        col3, col4 = st.columns(2)
        default_date = datetime.now(tz=timezone.utc).date()
        with col3:
            start_date = st.date_input("Start Date", value=default_date)
        with col4:
            end_date = st.date_input("End Date", value=default_date)

        submitted = st.form_submit_button("Search", type="primary")

    # Close container
    st.markdown("</div>", unsafe_allow_html=True)

    # -- Handle form submission
    if submitted:
        if not uploaded_file:
            st.error("Please upload a valid GeoJSON/JSON file first.")
            return

        bbox = extract_bbox(uploaded_file)
        if bbox is None:
            st.error("Could not parse bounding box from the uploaded file.")
            return

        st.success(f"Extracted Bounding Box: {bbox}")

        # Search for items
        if product_type == "truecolor":
            file_info = search_truecolor_items(bbox, start_date, end_date, cloud_cover)
        else:
            file_info = search_sar_items(bbox, start_date, end_date)

        if not file_info:
            st.warning("No matching satellite files found.")
        else:
            st.subheader("Available Files")
            display_download_links(file_info)

if __name__ == "__main__":
    main()
