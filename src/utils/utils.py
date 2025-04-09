"""Utility functions for data extraction and processing."""

import logging
from argparse import Namespace

from pystac_client import Client


def search_items(args: Namespace) -> list:
    """Search for STAC items using the provided arguments.

    Expected attributes on 'args':
      - start_date (str): Start date in YYYY-MM-DD format.
      - end_date (str): End date in YYYY-MM-DD format.
      - bbox (str): Bounding box as "min_lon,min_lat,max_lon,max_lat".
      - collections (list): List of collection IDs to search.
      - cloud_cover (int, optional): Maximum cloud cover percentage (if applicable).

    Returns:
      A list of STAC items matching the search criteria.
    """
    catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    bbox = [float(x) for x in args.bbox.split(",")]
    query = {}
    if getattr(args, "cloud_cover", None) is not None:
        query = {"eo:cloud_cover": {"lt": args.cloud_cover}}
    search = catalog.search(
        collections=[args.collection],
        bbox=bbox,
        datetime=f"{args.start_date}/{args.end_date}",
        query=query,
    )
    items = list(search.items())
    logging.info("Found %d items", len(items))
    return items
