
# Academic Research Automation Tools

This repository contains two Python scripts designed to automate various aspects of academic research analysis, specifically targeting citation data and publication records from Google Scholar. Each script serves a unique purpose, enabling users to gather and analyze data efficiently for academic papers and authors.

## Scripts Overview

### profile.py

- **Purpose**: Automates the process of retrieving citation counts and metrics for specific academic papers and authors from Google Scholar.
- **Key Features**:
  - Automated citation retrieval based on paper titles and author names.
  - Yearly citation analysis for total citations, and citations over the last 5 and 10 years.
  - Data aggregation into an Excel file for further analysis.

### scholar.py

- **Purpose**: Facilitates the extraction of publication data based on author names, journal names, and publication years, updating an Excel file with the results.
- **Key Features**:
  - Automated Google Scholar searches based on predefined criteria.
  - Extraction of publication data including author names, publication years, and journal names.
  - Updates an Excel file with search results for analysis.

## Common Dependencies

Both scripts require Python 3.x and several Python libraries for HTTP requests, HTML parsing, and data manipulation:

- `BeautifulSoup` (from `bs4`)
- `pandas`
- Other libraries like `urllib`, `gzip`, `datetime`, and `re` may also be required depending on the script.

## Installation

Ensure Python 3.x is installed on your system and install the required libraries using pip:

```sh
pip install beautifulsoup4 pandas
```

## Usage

Place each script in the same directory as your data files (Excel files for input and output data). Run each script via the command line or terminal as follows:

```sh
python profile.py
python scholar.py
```

Ensure you've prepared the input Excel files according to each script's requirements before running them.
