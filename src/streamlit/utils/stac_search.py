"""Searches for truecolor satellite items using the provided bounding box and date."""

from argparse import Namespace

from planetary_computer import sign

import streamlit as st
from src.data_extraction.utils.utils import search_items


def search_truecolor_items(
    bbox: list,
    start_date: str,
    end_date: str,
    cloud_cover: float,
) -> list:
    """Searches for truecolor satellite items using the provided bounding box and date.

    Returns a list of tuples with file names and URLs.
    """
    args = Namespace(
        collection="sentinel-2-l2a",
        product="truecolor",
        start_date=str(start_date),
        end_date=str(end_date),
        bbox=",".join([str(c) for c in bbox]),
        output_dir="",  # Not used for Streamlit
        cloud_cover=cloud_cover,
    )

    st.info("Searching for truecolor items...")
    try:
        items = search_items(args)
    except FileNotFoundError as e:
        st.error(f"Search failed: {e}")
        return []

    if not items:
        st.error("No items found.")
        return []

    file_info = []
    for item in items:
        signed_item = sign(item)
        asset = signed_item.assets.get("visual")  # For truecolor images
        if asset:
            file_name = f"{signed_item.id}_truecolor.tif"
            file_info.append((file_name, asset.href))
    return file_info


def search_sar_items(
    bbox: list,
    start_date: str,
    end_date: str,
) -> list[tuple[str, str]]:
    """Searches Sentinel-1 RTC (SAR) items using the provided bounding box and date.

    Returns a list of tuples with file names and URLs for the VV and VH polarizations.
    """
    st.info("Searching for Sentinel-1 SAR items...")

    args = Namespace(
        collection="sentinel-1-rtc",
        start_date=str(start_date),
        end_date=str(end_date),
        bbox=",".join([str(c) for c in bbox]),
        cloud_cover=None,
    )

    # 2. Perform the search using your existing utility
    items = search_items(args)

    if not items:
        st.error("No Sentinel-1 SAR items found.")
        return []

    # 3. Sign the items and extract the VV/VH asset links
    file_info = []
    for item in items:
        signed_item = sign(item)
        for pol in ["vv", "vh"]:
            asset = signed_item.assets.get(pol)
            if asset:
                file_name = f"{signed_item.id}_{pol}.tif"
                file_info.append((file_name, asset.href))

    return file_info
