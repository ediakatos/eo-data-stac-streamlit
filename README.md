# EO Data STAC Streamlit

This project is a Streamlit application for searching and downloading satellite imagery using the STAC API. It provides a user-friendly interface for specifying search criteria and viewing results.

## Features

- Upload GeoJSON files to define areas of interest.
- Search for satellite imagery by product type, date range, and cloud cover.
- Download results directly from the app.

## Documentation

Detailed documentation for each script can be found in the `doc/` directory:

- [app.py](doc/app.md): Main Streamlit application.
- [download_links.py](doc/download_links.md): Utility functions for generating download links.
- [geojson_utils.py](doc/geojson_utils.md): Functions for handling GeoJSON files.
- [stac_search.py](doc/stac_search.md): Functions for searching satellite imagery.
- [utils.py](doc/utils.md): General utility functions.

## Getting Started

1. Clone the repository.
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Run the application:
   ```bash
   make app
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
