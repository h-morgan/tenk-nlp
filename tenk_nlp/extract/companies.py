import requests
import json
from loguru import logger
import os

SEC_API_IO_API_KEY = os.getenv("SEC_API_IO_API_KEY")


def get_all_companies():

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
