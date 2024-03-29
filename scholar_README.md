
# Google Scholar Author Publication Counter

This Python script (`scholar.py`) automates the retrieval of publication data from 
Google Scholar.It fetches publications based on author names, journal names, 
and publication years, then updates an Excel file with the collected data.
This tool is particularly useful for compiling and analyzing academic outputs 
from specific journals within a defined time frame.

## Features

- **Automated Search**: Conducts automated searches on Google Scholar based on predefined criteria.
- **Data Extraction**: Extracts publication data including author names, publication years, and journal names.
- **Excel Integration**: Updates an Excel file with the search results for further analysis.

## Dependencies

- `BeautifulSoup` (from `bs4`): For parsing HTML content.
- `pandas`: For handling Excel file operations.
- `urllib`: For making HTTP requests to Google Scholar.
- `gzip`: For decompressing gzip-encoded content.
- `datetime`: For timestamping operations.
- `re`: For regular expression operations.

Ensure you have Python 3.x installed and install the necessary libraries using:

```sh
pip install beautifulsoup4 pandas
```

## Setup

1. Run profile.py to get the links of all the authors you need beforehand. This data will be stored in a file `test.xlsx`
2. Ensure `scholar.py` and the Excel file are in the same directory.

## Usage

Run the script from your command line or terminal:

```sh
python scholar.py
```

The script will perform searches based on the input data from the Excel file and update the same file with the results.
