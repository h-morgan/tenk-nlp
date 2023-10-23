import json
import os
from datetime import datetime
from ftplib import FTP

from loguru import logger
from tenk_nlp.db import database
from tenk_nlp.utils import utils


class ETLtenk:
    def __init__(self, batch_size: int = 100, year: int = 2023):
        self.batch_size = batch_size
        self.now = datetime.utcnow()
        # year is year of which to process 10ks
        self.year = year

    def extract_edgar_data(self):
        """Extract 10ks from SEC EDGAR"""
        ...

    def transform_edgar_data(self, data):
        """Transform edgar data from SEC 10k reports into raw db format"""
        ...

    def load_raw(self, data):
        """Load raw SEC EDGAR 10k data into raw db"""
        ...

    def run(self):
        logger.info("Starting ETL pipeline for 10K data.")
        # TODO: implement ETL for 10ks

    def download_10k_filings(cik, output_directory):
        # Connect to the SEC's EDGAR FTP server
        ftp = FTP("ftp.sec.gov")
        ftp.login()

        try:
            # Navigate to the directory containing 10-K filings for the given CIK
            ftp.cwd(f"/edgar/data/{cik}")

            # List the available filings
            filings = ftp.nlst()

            # Create the output directory if it doesn't exist
            os.makedirs(output_directory, exist_ok=True)

            for filing in filings:
                # Check if the filing is a 10-K (you may need to adapt the logic for your specific use case)
                if "10-K" in filing:
                    # Construct the full path for the filing on the FTP server
                    ftp_path = f"/edgar/data/{cik}/{filing}"

                    # Construct the local file path where the filing will be saved
                    local_file_path = os.path.join(output_directory, filing)

                    # Download the filing
                    with open(local_file_path, "wb") as file:
                        ftp.retrbinary(f"RETR {ftp_path}", file.write)

        finally:
            # Close the FTP connection
            ftp.quit()
