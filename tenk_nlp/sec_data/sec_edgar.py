import feedparser
from datetime import datetime

# Helium API updates as of 11/2021 require passing User-Agent param in header in requests - mocking a browser here
HEADERS = {
    "User-Agent": "Haley Morgan haley@promarconstruction.com",
    "Accept-Encoding": "gzip, deflate",  # This is another valid field
}


def retrieve_recent_10k_filings():
    # Define the URL for the EDGAR RSS feed of 10-K filings
    rss_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=10-K&count=1000&output=atom"

    # Parse the RSS feed
    feed = feedparser.parse(rss_url, request_headers=HEADERS)

    recent_10k_filings = []
    for entry in feed.entries:
        filing_date = entry.updated  # Date of the filing
        company_name = entry.title  # Title contains the company name and CIK number
        filing_link = entry.link  # Link to the filing details

        # Format the filing date as a Python datetime object
        filing_date = datetime.strptime(filing_date, "%Y-%m-%dT%H:%M:%S%z")

        # Extract CIK number from the title (if available)
        cik_number = None
        if "CIK" in company_name:
            cik_index = company_name.index("CIK") + 4
            cik_number = company_name[cik_index : cik_index + 10]

        recent_10k_filings.append(
            {
                "Filing Date": filing_date,
                "Company Name": company_name,
                "CIK Number": cik_number,
                "Filing Link": filing_link,
            }
        )

    return recent_10k_filings


def go():
    # Example usage:
    recent_filings = retrieve_recent_10k_filings()

    for filing in recent_filings:
        print(f"Filing Date: {filing['Filing Date']}")
        print(f"Company Name: {filing['Company Name']}")
        print(f"CIK Number: {filing['CIK Number']}")
        print(f"Filing Link: {filing['Filing Link']}\n")
