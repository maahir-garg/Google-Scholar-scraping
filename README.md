# Google Scholar scraping

Two Python scripts that collect publication counts and citation figures from Google Scholar and write them to Excel. They were built to support an economics research project.

## Context and status

The scripts were written between November 2023 and February 2024 as research-support tooling. They are kept for reference and are not maintained. Google Scholar markup and access rules change, so the scripts may no longer work as written.

## What is in the repo

- `profile.py`: looks up Google Scholar author profiles for a list of papers and authors, and computes each author's citation counts before the year of the paper.
- `scholar.py`: for each author in a spreadsheet, counts their publications in five economics journals (American Economic Review, Econometrica, Quarterly Journal of Economics, Review of Economic Studies, Journal of Political Economy) over three windows.
- `requirements.txt`: the third-party libraries the scripts import.
- `.env.example`: the environment variable the scripts read, with no value.

## Requirements and setup

Python 3 and the packages in `requirements.txt` (`beautifulsoup4`, `pandas`, `requests`). Reading and writing `.xlsx` files through pandas also needs an Excel engine such as `openpyxl`, which is not imported directly and so is not in `requirements.txt`.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt openpyxl
```

Configuration: the scripts send a `Cookie` header taken from the `GOOGLE_SCHOLAR_COOKIE` environment variable, and omit the header if it is not set. The value is never stored in the repository. To use the scripts, copy a current session value from your own browser into the environment variable (see `.env.example`). Do not commit it.

## Usage

Both scripts read and write files in the current directory, and neither takes command-line arguments. The input spreadsheets are not included in the repository.

`profile.py`

- Reads `test.xlsx`, which needs the columns `Paper Title`, `Author Name` and `Year`, plus `l`, `a`, `b` and `c` for the merge step.
- `final_run()` searches Scholar for each unique paper, follows the author profile links found, and appends rows to an existing `task2.xlsx`. That file must already exist, with seven columns in this order: author name, paper title, year, total citations, citations in the last 5 years, citations in the last 10 years, profile link. The columns read back by the merge step are named `Author Name`, `Paper Title`, `Number of Citations total`, `Number of Citations last 5`, `Number of Citations last 10` and `Link`.
- The counts are the profile owner's citations by year, taken from the profile's citation histogram: total before the paper's year, and the 5 and 10 years before it. They are author-level figures, not per-paper citations.
- `merge_files()` copies those figures and the profile link from `task2.xlsx` into columns `a`, `b`, `c` and `l` of `test.xlsx`, matching on paper title and author name.
- The calls to `final_run()` and `merge_files()` at the bottom of the file are commented out. Uncomment the one you want before running `python profile.py`; as shipped, the script only prints two timestamps.

`scholar.py`

- Reads `test.xlsx`, which needs the columns `Author Name`, `Author Name New`, `l` (the profile link produced by `profile.py`), `Year`, `Error`, and for each journal the columns `<journal> full`, `<journal> last 5` and `<journal> last 10`.
- Running `python scholar.py` starts `running()` immediately. For each row with a profile link, it runs an advanced Scholar search per journal and counts results that match the author's profile ID, appear in an accepted publisher, are not marked as revised, and do not have a title containing "comment", "note", "reply", "correction" or "symposium". The three windows are everything up to the year before the paper, and the 5 and 10 years up to that year.
- It writes the filled-in table to the file named in the `filename` variable in `running()`, and also saves partial results if a request fails.
- `testing()` and `updating_Author_name()` are helper functions that are not called.

## Notes and limits

- Automated access to Google Scholar is restricted by its terms of service, and Scholar throttles or blocks automated requests. The scripts sleep between requests, but they have no retry logic and stop at the first failed request.
- Only the first results page is parsed. When a search reports more than 10 results, the journal name is appended to the `Error` column for manual checking.
- Name matching in `profile.py` falls back to first-name or last-name substring matches, so merged rows should be checked by hand.
- The data comes from Google Scholar at the time of each run and is not included here. Output depends on the input spreadsheets, which you must supply.
