import click
from loguru import logger

from tenk_nlp.keywords.keyword_gen import run_keyword_generator
from tenk_nlp.summarizers.summarizer import Summarizer
from tenk_nlp.summarizers.models import load_model


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "-m",
    "--model",
    default="BART",
    type=click.Choice(["BART", "GPT"]),
    help="Which api/summarization model to use.",
)
@click.option(
    "-l", "--length", default=850, help="Desired output summary length, in tokens"
)
def summarize(model, length):

    # TODO: build logic to get text from somehwere - has to be less than 1024 tokens at a time
    text = ""
    with open("temp/aapl_risks.txt", "r") as f:
        # text2 = f.read()
        for line in f:
            if len(text) < 5000:
                text += line
            else:
                break

    # with open("temp/aapl_risks.txt", "r") as f:
    #    text = f.read()

    logger.info(
        f"Performing summarization on Apple 10-K, Risks section, length of original text = {len(text)}"
    )

    model = load_model(model)

    # instantiate the summarizer class selected by user
    # model = sum_map[model]()
    summarizer = Summarizer(model=model)

    # summarize the text
    summary = summarizer.summarize_recursive(text, length)
    print(summary)


@click.command()
@click.option("-n", "--number", default=15, help="Number of keywords to generate")
def keywords(number):

    # TODO: build logic to get text from somehwere - has to be less than 1024 tokens at a time
    with open("temp/aapl_risks.txt", "r") as f:
        text = f.read()

    kw = run_keyword_generator(text, number_of_kw=number)

    print(kw)


cli.add_command(summarize)
cli.add_command(keywords)
