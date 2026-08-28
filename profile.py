import os
# Import necessary libraries
import random
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import quote_plus
import urllib.request
import gzip
import pandas as pd
from io import BytesIO
import datetime


# Function to retrieve links from Google Scholar based on a paper title and an author's name.
# This helps in identifying specific scholarly articles and their citation information.
def get_links(paper, one_author):
    # Construct search URL with parameters for paper title and author name
    url = 'https://scholar.google.com/scholar?as_q=&as_epq=' + paper + "&as_oq=&as_eq=&as_occt=any&as_sauthors=" + one_author + "&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C5"
    url = quote_plus(url, safe='/:?=&')
    print(url)
    # Headers to mimic a browser request, avoiding potential blocking by Google Scholar
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
    }
    cookie = os.getenv("GOOGLE_SCHOLAR_COOKIE")
    if cookie:
        headers["Cookie"] = cookie
    # Make the request to Google Scholar with prepared URL and headers
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    # If the response is compressed with gzip, decompress it
    if response.info().get('Content-Encoding') == 'gzip':
        gzip_file = gzip.GzipFile(fileobj=BytesIO(response.read()))
        decompressed_content = gzip_file.read()
    else:
        decompressed_content = response.read()
    # Decode response content to UTF-8
    html_content = decompressed_content.decode('utf-8')
    response.close()
    # Parse HTML content with BeautifulSoup to find necessary data
    soup = BeautifulSoup(html_content, 'html.parser')
    refined_soup = soup.find('div', class_='gs_r gs_or gs_scl')

    # Logic to refine search results to find specific citation links
    # and handle different page structures
    if refined_soup:
        pass
    else:
        refined_soup = soup.find('div', class_='gs_r gs_or gs_scl gs_fmar')

    # If a valid section is found, extract citation links
    if refined_soup:
        citation_link = refined_soup.find_all(
            lambda tag: tag.name == "a" and tag.get("href") and "/citations?user=" in tag.get("href"))

        if citation_link:
            link_lists = []
            for link in citation_link:
                citation_url = link.get("href")
                final_url = urljoin("https://scholar.google.com", citation_url)
                if final_url in link_lists:
                    pass
                else:
                    link_lists.append(final_url)
                    print("User: ", final_url)
                    pass
                pass
            print("*"*20)
            return link_lists
        else:
            return None
    # If no links found with specific author, retry without author
    else:
        return get_links(paper, "")


# The `citations_per_paper` function extracts and calculates citation metrics from the author's profile page.
def citations_per_paper(links, year_given):
    # Initialize a list to store citation data for each link (author profile)
    to_ret = []
    # Iterate over each link (author profile) to extract citation data
    for link in links:
        # Setup request headers and make the request to Google Scholar
        # Headers are used to mimic a browser request for successful scraping
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
        }
        cookie = os.getenv("GOOGLE_SCHOLAR_COOKIE")
        if cookie:
            headers["Cookie"] = cookie
        # Make the request to Google Scholar with prepared URL and headers
        req = urllib.request.Request(link, headers=headers)
        response = urllib.request.urlopen(req)
        # If the response is compressed with gzip, decompress it
        if response.info().get('Content-Encoding') == 'gzip':
            gzip_file = gzip.GzipFile(fileobj=BytesIO(response.read()))
            decompressed_content = gzip_file.read()
        else:
            decompressed_content = response.read()
        # Decode response content to UTF-8
        html_content = decompressed_content.decode('utf-8')
        response.close()
        # Parse HTML content with BeautifulSoup to find necessary data
        soup = BeautifulSoup(html_content, 'html.parser')
        name = soup.find('div', id='gsc_prf_in').text
        print(name)

        tot_cit_div = soup.find('td', class_='gsc_rsb_std')
        tot_cit = int(tot_cit_div.text)

        # Initialize a dictionary to hold citation counts by year
        citation_counts = {}
        graph_div = soup.find('div', class_='gsc_md_hist_b')

        # If citation data by year is available, parse and store it in citation_counts
        if graph_div:
            years = [span.text for span in graph_div.find_all('span', class_='gsc_g_t')]
            counts = [int(span.text.replace(',', '')) for span in graph_div.find_all('span', class_='gsc_g_al')]
            citation_counts = dict(zip(years, counts))

        # Calculate total citations and citations within 5 and 10 year ranges
        total_citations = tot_cit - sum(citation_counts[year] for year in citation_counts if int(year) >= year_given)
        total_citations_5 = sum(citation_counts[year] for year in citation_counts if (int(year) in range(year_given-5, year_given)))
        total_citations_10 = sum(citation_counts[year] for year in citation_counts if (int(year) in range(year_given-10, year_given)))
        # Append the extracted data for this author to the return list
        to_ret.append([name, total_citations, total_citations_5, total_citations_10, link])
        print("-" * 20)
    # Return the collected citation data for all processed authors
    return to_ret


# The `final_run` function orchestrates the overall process, reading an input Excel file,
# fetching data for each paper and author, and then writing the results to a new Excel file.
def final_run():
    # Load the initial dataset from an Excel file
    file = pd.read_excel("test.xlsx")
    papers_unique = {}

    # Extract unique papers and their corresponding authors and publication years
    for i in range(len(file["Paper Title"])):
        paper = file["Paper Title"][i]
        author = file["Author Name"][i]
        year = file["Year"][i]

        # Avoid processing the same paper more than once
        if paper in papers_unique.keys():
            pass
        else:
            papers_unique[paper] = [author, year]

    # Prepare a new DataFrame for the output
    final_table = pd.read_excel("task2.xlsx")

    # For each unique paper, fetch the relevant citation data
    for paper in papers_unique.keys():
        print(paper)

        # Retrieve links to the authors' Google Scholar profiles
        links = get_links(paper, papers_unique[paper][0])

        # If links are found, fetch and process citation data
        if links:
            values = citations_per_paper(links, papers_unique[paper][1])
            for value in values:
                # Construct a new entry for the output DataFrame
                entry = [value[0], paper, papers_unique[paper][1]] + value[1:]
                print(entry)
                # Append the new entry to the final table
                final_table.loc[len(final_table.index)] = entry
                pass
            print("**"*20)
            pass

    # Output the final table to an Excel file
    print(final_table)
    final_table.to_excel("task2.xlsx", index=False)


# Combines the newly generated citation data with the original dataset.
def merge_files():
    file1 = pd.read_excel("test.xlsx")
    file2 = pd.read_excel("task2.xlsx")

    # Data preparation for merging
    file1["l"] = file1["l"].astype(str)
    j_count = len(file1.index)
    i_count = len(file2.index)
    j_used = []

    # Iterate through the new data to find matches in the original dataset
    for i in range(i_count):
        print(i)
        found_name = file2["Author Name"][i].lower()
        print(found_name)
        for j in range(j_count):
            # Skip already processed or non-matching entries
            if (j in j_used) or file1["Paper Title"][j] != file2["Paper Title"][i]:
                pass
            else:
                given_name = file1["Author Name"][j].lower()
                print(given_name)
                # If a matching author and paper title are found, update the original dataset with the new citation data
                if found_name == given_name:
                    file1.at[j, "a"] = file2["Number of Citations total"][i]
                    file1.at[j, "b"] = file2["Number of Citations last 5"][i]
                    file1.at[j, "c"] = file2["Number of Citations last 10"][i]
                    file1.at[j, "l"] = file2["Link"][i]
                    j_used.append(j)
                    print("-" * 20)
                    break
                elif found_name.split()[0] in given_name:
                    file1.at[j, "a"] = file2["Number of Citations total"][i]
                    file1.at[j, "b"] = file2["Number of Citations last 5"][i]
                    file1.at[j, "c"] = file2["Number of Citations last 10"][i]
                    file1.at[j, "l"] = file2["Link"][i]
                    j_used.append(j)
                    print("-" * 20)
                    break
                elif found_name.split()[-1] in given_name:
                    file1.at[j, "a"] = file2["Number of Citations total"][i]
                    file1.at[j, "b"] = file2["Number of Citations last 5"][i]
                    file1.at[j, "c"] = file2["Number of Citations last 10"][i]
                    file1.at[j, "l"] = file2["Link"][i]
                    j_used.append(j)
                    print("-" * 20)
                    break

        print("*"*20)
    file1.to_excel("test.xlsx", index=False)


# Example usage and execution timestamps
print(datetime.datetime.now())
# Uncomment to run the main function
# final_run()
# Uncomment to merge the resulting data with the original input
# merge_files()
print(datetime.datetime.now())
