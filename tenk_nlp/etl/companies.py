import json
import os
from datetime import datetime

import requests
from loguru import logger
from tenk_nlp.db import database
from tenk_nlp.utils import utils

SEC_API_IO_API_KEY = os.getenv("SEC_API_IO_API_KEY")


def update_company_files():

    exchanges = ["NYSE", "NASDAQ", "NYSEMKT", "NYSEARCA", "OTC", "BATS", "INDEX"]

    header = {"Authorization": SEC_API_IO_API_KEY}

    # create output dir if necessary
    output_dir = "data/companies"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.debug(f"Output directory {output_dir} created")

    # make request to get a list of companies on every exchange
    for exchange in exchanges:
        logger.info(f"Getting company info for all companies on {exchange} exchange")
        url = f"https://api.sec-api.io/mapping/exchange/{exchange}"
        response = requests.get(url, headers=header)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Retrieved {len(data)} companies for {exchange} exchange")

            with open(f"{output_dir}/{exchange}.json", "w") as fp:
                json.dump(data, fp)
        else:
            logger.error(f"Could not make successful request for url {url}")
            logger.error(f"{response.status_code}: {response.text}")

    logger.info(
        f"Company info retrieval from sec-api.io complete for {len(exchanges)} exchanges."
    )


class ETLcompanies(BaseETLpipeline):
    def __init__(self):
        self.now = datetime.utcnow()
        # metrics
        self.transform_no_cik = 0
        self.transform_delisted = 0

    def extract(self):
        """Extract company data from JSON files saved in the data/companies/ dir"""
        data_dir = "data/companies/"
        files = self.get_files_from_dir(data_dir)

        for f in files:
            with open(f) as next_file:
                data = json.load(next_file)
                yield data

    def transform(self, data):
        """Transform company data file contents into db-writeable values"""
        for company in data:
            # minor cleaning - only keep companies that have a value for CIK # (these are the only ones we can retrieve 10ks for anyways)
            if company["cik"] in {None, ""}:
                logger.debug(
                    f"[Exchange: {company['exchange']}] Company {company['name']} does not have CIK value:[{company['cik']}], skipping"
                )
                self.transform_no_cik += 1
                continue
            # don't include any companies that have been delisted
            if company["isDelisted"] in {"True", "true", True, 1}:
                logger.debug(
                    f"[Exchange: {company['exchange']}] Company {company['name']} is delisted (or has delisted entry), skipping"
                )
                self.transform_delisted += 1
                continue

            # create uuid and replace the 'id' field with our own generated uuid
            this_id = utils.md5hex_from_json(company)
            company["id"] = this_id
            company["updated_at"] = self.now
            yield company

    def load(self, data):
        """Load the company data into the database"""

        company_value = {
            "id": data["id"],
            "name": data["name"],
            "cik": data["cik"],
            "cusip": data["cusip"],
            "exchange": data["exchange"],
            "is_delisted": data["isDelisted"],
            "category": data["category"],
            "sector": data["sector"],
            "industry": data["industry"],
            "sic": data["sic"],
            "sic_sector": data["sicSector"],
            "sic_industry": data["sicIndustry"],
            "fama_sector": data["famaSector"],
            "fama_industry": data["famaIndustry"],
            "currency": data["currency"],
            "location": data["location"],
            "updated_at": data["updated_at"],
        }

        database.upsert_company(company_value)

    def run(self):
        logger.info("Starting ETL pipeline for company data.")
        # if extract_only, saves copy of extracted data to local dir (dev) or s3 (prod)
        processed_companies = 0
        for extracted_batch in self.extract():
            for transformed_company in self.transform(extracted_batch):
                self.load(transformed_company)
                processed_companies += 1

        logger.info(f"Proccesed {processed_companies} new or updated companies.")
        logger.info(f"Skipped {self.transform_delisted} delisted companies.")
        logger.info(f"Skipped {self.transform_no_cik} companies without CIK#s")
        logger.info("Company data ETL pipeline complete.")

    def get_files_from_dir(self, dirname: str) -> list[str]:
        if os.path.exists(dirname) and os.path.isdir(dirname):
            files = [
                os.path.join(dirname, f)
                for f in os.listdir(dirname)
                if os.path.isfile(os.path.join(dirname, f))
            ]
            logger.debug(f"Retrieved {len(files)} files from {dirname}")
            return files
        else:
            logger.debug(f"No files found in requested dir: {dirname}")
            return []
