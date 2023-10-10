# 10-K NLP

This is a service that performs various natural language processing techniques to public company's 10-K reports. The service performs keyword generation and summarization on various sections of the report as requested.

Note: this service is still under construction, so functionality isn't complete yet.

## Requirements and Setup

- python 3.11
- poetry

If you're running this for the first time or from a new machine, after cloning the repo run:

```bash
poetry install
```

Now you can run any available poetry cli commands, as defined in the pyproject.toml file.

## How to run cli commands

Run any of the commands with `--help` after them to get the most up to date args info.

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
