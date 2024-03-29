# Import necessary libraries
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus
import urllib.request
import gzip
from io import BytesIO
import time
import random
import datetime
import re

# Defines a dictionary mapping journal names to their publication links.
# This is used to filter search results to specific journals.
publicationLinks = {"American Economic Review": ["aeaweb.org", "JSTOR", "pubs.aeaweb.org"],
                    "Econometrica": ["Wiley Online Library", "JSTOR"],
                    "Quarterly Journal of Economics": ["academic.oup.com", "jstor"],
                    "Review of Economic Studies": ["academic.oup.com"],
                    "Journal of Political Economy": ["journals.uchicago.edu", "jstor"]}

# Reads an Excel file into a DataFrame for processing.
final_file = pd.read_excel("test.xlsx")
more_than_10 = []


# Defines a function to retrieve publications from Google Scholar based on author name,
# journal name, publication year range, and a unique user ID for each author.
def get_scholar_publications(author_name, journal_name, start_year, end_year, user_id, index):
    journal_links = publicationLinks[journal_name]
    # Constructs the search URL with specified parameters.
    link = "https://scholar.google.com/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=" + author_name + "&as_publication=" + journal_name + "&as_ylo=" + str(
        start_year) + "&as_yhi=" + str(end_year) + "&hl=en&as_sdt=0%2C5&as_vis=1"
    link = quote_plus(link, safe='/:?=&')
    print(link)
    # Headers to mimic a browser request to avoid being blocked by Google Scholar.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
        "Server": "scholar",
        "Refer": "https://scholar.google.com/schhp?hl=en",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Cookie": 'GOOGLE_ABUSE_EXEMPTION=ID=f83fb44e56358633:TM=1709558664:C=r:IP=137.132.26.113-:S=oaedhAhrWESENrjog7sNhXo; GSP=A=ydeQ-A:CPTS=1709558665:LM=1709558665:S=yLS9ikJhdz_Q8Hb0; NID=512=L_FiR8ux3YdD2cwqCYJj9aXfvhgtDow0XfuG48mZ0Rv5E2JQGbpDDPOZo_eqK8cTdopGyhcQwZqrALw0rASHQrzzFYa9QaO2IPUJJQp0KGODBN889Zg8V5MwcEfPGWCoXRw68OPYf5owMZ0iolaq1GaA5Dp07-oRIq8CPkJ4oWM'}

    # Error handling for HTTP requests.
    try:
        req = urllib.request.Request(link, headers=headers)
        response = urllib.request.urlopen(req)
    except HTTPError as e:
        print(e)
        return None

    # Decompresses the response if it's gzip-encoded.
    if response.info().get('Content-Encoding') == 'gzip':
        gzip_file = gzip.GzipFile(fileobj=BytesIO(response.read()))
        decompressed_content = gzip_file.read()
    else:
        decompressed_content = response.read()
    html_content = decompressed_content.decode('utf-8')
    response.close()

    # Parses the HTML content to extract the number of publications.
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)
    result_stats = soup.find("div", {"id": "gs_ab_md"})

    num_publications = 0

    if result_stats.text:
        num_publications = result_stats.text.split()[0]
        if num_publications == "About":
            num_publications = int(result_stats.text.split()[1])
        else:
            num_publications = int(num_publications)

    # Logic to handle publications exceeding a certain count and to filter results based on specific criteria.
    if 0 < num_publications:
        if num_publications > 10:
            if index in more_than_10:
                pass
            else:
                more_than_10.append(index)
            print("check for more than 10:", num_publications-10, "more papers to see")
            if pd.isnull(final_file["Error"][index]):
                final_file["Error"][index] = journal_name
            else:
                final_file["Error"][index] += " " + journal_name
        all_articles = soup.find_all("div", class_="gs_r gs_or gs_scl")
        num_of_articles = len(all_articles)
        print("Number of articles found:", num_of_articles)
        if num_of_articles == 0:
            return None
        for publication in all_articles:
            paper_name = publication.find('h3', class_='gs_rt').text
            given_authors = publication.find_all(
                lambda tag: tag.name == "a" and tag.get("href") and "/citations?user=" in tag.get("href"))
            journal_name = publication.find('div', class_='gs_a').text
            paper_abstract = publication.find('div', class_='gs_rs').text
            is_correct_publication = False
            for correctJournalName in journal_links:
                if correctJournalName.lower() in journal_name.lower():
                    is_correct_publication = True
                    break
            is_correct_author = False
            for links in given_authors:
                url = links.get("href")
                if user_id in url:
                    is_correct_author = True
                    break
            is_not_revised = True
            if "revised" in paper_abstract.lower():
                is_not_revised = False
            correct_title = True
            for incorrect_word in ["comment", "note", "reply", "correction", "symposium"]:
                if incorrect_word in paper_name.lower():
                    correct_title = False
            if is_correct_author and is_correct_publication and is_not_revised and correct_title:
                pass
            else:
                print("*" * 10)
                print(paper_name)
                if not is_correct_publication:
                    print(is_correct_publication, "publication")
                    print(journal_name)
                if not is_correct_author:
                    print(is_correct_author, "author")
                    print(given_authors)
                if not is_not_revised:
                    print("revised")
                if not correct_title:
                    print("Invalid Title")
                print("*" * 10)
                num_publications -= 1

    return num_publications


def running():
    filename = "Test_X_Ziqiu Edited.xlsx"
    journal_list = ["American Economic Review", "Quarterly Journal of Economics", "Econometrica",
                    "Review of Economic Studies",
                    "Journal of Political Economy"]
    columns = [" full", " last 5", " last 10"]

    # Loops through each row in the loaded Excel DataFrame to process each author.
    for i in range(len(final_file["Author Name"])):
        link = final_file["l"][i]
        # If a link exists, extract the unique user ID from it and proceed.
        if pd.isnull(link):
            pass
        else:
            match = re.search(r"(?<=user=)(.*?)(?=&|$)", link)
            user_id = match.group(1)
            # Introduces a delay after every 10 iterations to prevent overloading the server.
            if i % 10 == 0:
                time.sleep(10)
            print("-" * 50)
            author_name = final_file["Author Name New"][i]
            print(f'{i}: {author_name}')
            print(user_id)
            year = final_file["Year"][i] - 1
            # For each journal, fetches the publication data for the given author and updates the DataFrame.
            for journal in journal_list:
                j = 0
                wait_time = random.randint(4, 7)
                print(f"{wait_time}-" * 20)
                time.sleep(wait_time)
                for col in columns:
                    # Custom logic based on the column being processed (full, last 5, last 10 years).
                    # Fetches publication counts and updates the DataFrame accordingly.
                    col_name = journal + col
                    print(col_name)
                    if final_file[journal + " full"][i] == 0:
                        num_publications = 0
                    elif col == " full":
                        num_publications = get_scholar_publications(author_name=author_name, journal_name=journal,
                                                                    start_year="", end_year=year, user_id=user_id, index=i)
                    else:
                        time.sleep(random.randint(1, 3))
                        num_publications = get_scholar_publications(author_name=author_name, journal_name=journal,
                                                                    start_year=year - j + 1, end_year=year,
                                                                    user_id=user_id, index=i)
                    print(num_publications)
                    # something went wrong, error handling
                    if num_publications is not None:
                        final_file[col_name][i] = num_publications
                    else:
                        final_file.to_excel(filename, index=False)
                        return None
                    j += 5
                    pass
                pass
        pass
    # Saves the updated DataFrame back to the Excel file.
    final_file.to_excel(filename, index=False)


def testing():
    print(get_scholar_publications(author_name="ARIEL RUBINSTEIN", journal_name="Econometrica", start_year=1999,
                                   end_year=2008, user_id="sCccieYAAAAJ", index=42))
    final_file.to_excel("test.xlsx", index=False)
    pass


# Updates author names in the DataFrame for consistency, such as normalizing name formats.
def updating_Author_name():
    for i in range(len(final_file["Author Name"])):
        if pd.isnull(final_file["Author Name"][i]):
            pass
        else:
            author_name = final_file["Author Name"][i]
            first_name = author_name.split()[0].split(".")[0]
            last_name = author_name.split()[-1].split(".")[-1]
            if last_name == "":
                last_name = author_name.split()[-1].split(".")[-2]
            author_name = first_name + " " + last_name
            if len(first_name) == 1:
                final_file["New Comments"][i] = "Single first letter"
            if "jr" in author_name.lower():
                final_file["New Comments"][i] = "Jr in name"
            print(f'{i}: {author_name}')
            final_file["Author Name New"][i] = author_name
            if final_file["Author Name Updated"][i] != author_name:
                final_file["Similarity"][i] = "False"
    # Manually making these edits to maintain consistency
    final_file.to_excel("test.xlsx", index=False)


# Example usage of the `running` function to start the process.
print(datetime.datetime.now())
running()
print(more_than_10)
print(datetime.datetime.now())
