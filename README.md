# Google Scholar research-analysis scripts

This repository contains two Python scripts for collecting publication and citation information from Google Scholar and writing structured results for analysis.

## Scripts

- `profile.py` retrieves citation links and author-profile metrics for configured papers and authors.
- `scholar.py` searches for publication records using configured author, journal, and year criteria.

Both scripts parse HTML with Beautiful Soup and use pandas for tabular processing. See `profile_README.md` and `scholar_README.md` for script-specific input notes.

## Security

Optional request-session material is read from the `GOOGLE_SCHOLAR_COOKIE` environment variable.

- Never paste cookies, session values, or credentials into source code.
- Never commit a populated `.env` file.
- Revoke or invalidate exposed session material before using the repository.
- Run a full-history secret scan before treating the repository as clean.

The scripts omit the Cookie header when `GOOGLE_SCHOLAR_COOKIE` is not set.

## Requirements

- Python 3
- beautifulsoup4
- pandas
- openpyxl

Install the dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4 pandas openpyxl
```

If a current session value is required, keep it local:

```bash
cp .env.example .env
export GOOGLE_SCHOLAR_COOKIE="replace-with-a-current-local-value"
```

Run the scripts from the repository root:

```bash
python profile.py
python scholar.py
```

## Responsible use and limitations

Google Scholar can change its markup, throttle automated requests, or block traffic. Use conservative request rates, respect applicable terms and robots guidance, cache responses where appropriate, and validate all generated records. The repository does not provide a reproducible benchmark for time savings or data quality.
