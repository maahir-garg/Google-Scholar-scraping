
# Google Scholar Author Citation Counter

This Python script automates the process of retrieving and analyzing citation data 
for authors from Google Scholar. It facilitates the gathering of citation counts 
for specific authors, offering insights into academic impact over time.

## Features

- **Automated Citation Retrieval**: Fetches citation data from Google Scholar based on paper titles and author names.
- **Yearly Citation Analysis**: Calculates total citations, citations over the last 5 years, and citations over the last 10 years for each paper.
- **Data Aggregation**: Generates a consolidated report with citation metrics, aiding in the evaluation of research impact.

## Dependencies

This script requires Python 3.x and the following Python libraries:

- `requests`
- `BeautifulSoup` (from `bs4`)
- `pandas`
- `datetime`

These dependencies are necessary for making HTTP requests, parsing HTML content, data manipulation, and handling date and time, respectively.

## Installation

First, ensure Python 3.x is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).

Install the required Python libraries using pip by running the following command in your terminal:

```sh
pip install requests beautifulsoup4 pandas
```

## Usage

1. Prepare an input Excel file named `test.xlsx` with columns for "Paper Title", "Author Name", and "Year". This file will serve as the input dataset for the script.
2. Save the `profile.py` script in the same directory as your `test.xlsx` file.
3. Execute the script with Python by running:

```sh
python profile.py
```

The script will process the input data, retrieve citation metrics, and output the results to a new Excel file named `task2.xlsx`.
