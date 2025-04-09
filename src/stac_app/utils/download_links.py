"""Download links for files in Streamlit app."""

import streamlit as st


def display_download_links(file_info: list[tuple[str, str]]) -> None:
    """Displays clickable download links within an expander.

    Expects file_info as a list of tuples (file_name, url).
    """
    if not file_info:
        st.error("No downloadable files found.")
        return

    st.info("Files ready for download.")
    st.markdown("### Download Links")
    with st.expander("Click to view/download files"):
        for file_name, url in file_info:
            st.markdown(f"- [{file_name}]({url})", unsafe_allow_html=True)
