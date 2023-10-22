# 10-K NLP Data ETL Services

This repo holds functionality for the ETL services required to populate the database needed for the 10k NLP API. The logic in this repo includes:

- ETL for company data, 10K reports, and other related data from various sources
- Performing the NLP analysis on company 10Ks, including keyword generation and summarization

Note: this service is still under construction, so functionality isn't complete yet.

## Table of Contents

- [1. Data Sources and Processing](#1-data-sources-and-processing)
  - [1.1 Extract](#11-extract)
  - [1.2 Transform](#12-transform)
  - [1.3 Load](#13-load)
- [2. Requirements and Setup](#2-requirements-and-setup)
  - [2.1 Environment Variables](#21-environment-variables)
  - [2.2 Dev Database Connection](#22-dev-database-connection)
  - [2.3 Prod Database Connection](#23-prod-database-connection)
  - [2.4 Database Migrations](24-database-migrations)
- [3. How to use](#3-how-to-use)
  - [3.1 Data ETL](#31-data-etl)
  - [3.2 NLP](#32-nlp)
- [4. Running Tests](#4-running-tests)

## 1. Data Sources and Processing

### 1.1 EXTRACT

We get pre-processed data from 2 different sources:

1. [sec-api.io](https://sec-api.io/)
   - This is where we get company info for all companies on the following 7 exchanges: NYSE, NASDAQ, NYSEMKT, NYSEARCA, OTC, BATS, INDEX
   - We need company info to have an exhaustive (as possible) list of public companies, mapped to their CIK numbers. CIK numbers are how the SEC's EDGAR database stores and organizes company reports, and we need this CIK number to make requests to the EDGAR database for specific companies
2. [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch)
   - This is a public database maintained by the SEC, containing all public company filings
   - There is no LIST endpoint available for downloading company filings, so we have to make individual requests with each company's CIK # (hence the company mapping data referenced above)
   - We retrieve company 10K reports here and store the text output

### 1.2 TRANSFORM

Once we've retrieved a company's 10K report, we then apply some NLP techniques on various sections within the report. For the sections of interest, we perform the following:

- keyword extraction of key sections
- summarization of key sections using two different summarization models: BART and ChatGPT.

### 1.3 LOAD

We store both the raw pre-processed data (company information and 10K reports), and the transformed/processed data in a SQL database.

## 2. Requirements and Setup

- python 3.11
- poetry

If you're running this for the first time or from a new machine, after cloning the repo run:

```bash
poetry install
```

Now you can run any available poetry cli commands, as defined in the pyproject.toml file.

### 2.1 Environment Variables

The following environment variables may be required, depending on how you are using this service:

```
OPENAI_API_KEY= # ChatGPT / OpenAI API key, for requesting summaries from ChatGPT

SEC_API_IO_API_KEY= # sec-api.io API key, if performing company data extraction
```

### 2.2 Dev Database Connection

During development, we use a locally running sqlite database, and run the alembic migration to make sure the database has the latest updates.

That just requires 2 db env vars:

```
DB_DRIVER=sqlite
DB_HOST=/path/to/db/file/dev.db
```

Note: if this is your first time setting up your dev env, to create a sqlite db on a mac all you need to do is create a file with a `.db` extension, anywhere on your machine. You can then open any compatible database gui of your choice, like dbeaver, etc.

### 2.3 Prod Database Connection

When running on prod, we use a MySQL database, and the following env vars are required:

```
DB_DRIVER=mysql
DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=host
DB_PORT=3306
DB_NAME=prod
```

\*\*Replace values with actual prod db connection details

### 2.4 Database Migrations

If you're setting up a new database for the first time, you'll need to run the latest database migration. The command to do that is:

```bash
poetry run alembic upgrade head
```

To update the database schema, you'll need to generate a new migration. To do that, all you have to do is update the models in the [tenk_nlp/db/models.py file](tenk_nlp/db/models.py) and then run the following command, which will automatically generate a new migration in the [alembic/versions/](alembic/versions/) directory:

```bash
poetry run alembic revision --autogenerate -m 'migration description'
```

## 3. How to use

Run any poetry commands with `--help` after them to get the most up to date args info.

### 3.1 Data ETL

#### Get Company Data

Note: you will need to set the `SEC_API_IO_API_KEY` env variable to perform this command.

To retrieve a data dump of all company info on all exchanges, run the following:

```bash
poetry run extract_companies
```

This will save the company data in a data/companies/ directory.

### 3.2 NLP

To run the keyword generator, run the following command:

```bash
poetry run keywords
```

To run the summarizer:

```bash
poetry run summary
```

Optionally, you can provide the `-m` or `--model` argument to tell it which NLP model/service you want to use. The existing possible choices that have been implemented:

- `GPT`
- `BART`

## 4. Running tests

To run tests using pytest, run:

```bash
poetry run pytest
```
