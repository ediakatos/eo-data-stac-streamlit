"""Utility functions for processing GeoJSON files and extracting geometries."""

import json

import geopandas as gpd

import streamlit as st


def extract_bbox(uploaded_file: str) -> list:
    """Extracts the bounding box from an uploaded GeoJSON file.

    Returns the bounding box as [minx, miny, maxx, maxy] or None if an error occurs.
    """
    try:
        geojson_data = json.load(uploaded_file)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None

    if "features" in geojson_data:
        try:
            gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
        except (ValueError, KeyError) as e:
            st.error(f"Error processing GeoJSON features: {e}")
            return None
        else:
            return gdf.total_bounds  # [minx, miny, maxx, maxy]
    else:
        st.error("Invalid GeoJSON: Missing 'features'.")
        return None
