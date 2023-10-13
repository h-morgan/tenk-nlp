import os

from loguru import logger
import time
import openai
from transformers import pipeline


def load_model(model_name: str):

    if model_name == "BART":
        model = BARTModel()

    elif model_name == "GPT":
        model = ChatGPT()

    else:
        raise NotImplementedError(f"Requested model {model_name}This ")

    return model


class BARTModel:
    model_name: str = "BART"

    def __init__(self) -> None:
        self.model = self.load_model()

    def load_model(self):
        """Returns BART summarization model API that can be interacted with"""
        logger.info("Now loading BART model for NLP summarization")
        tic = time.perf_counter()
        model = pipeline("summarization", model="facebook/bart-large-cnn")
        toc = time.perf_counter()
        logger.debug(f"Summarizer model loaded in {toc-tic:0.4f} seconds")
        return model

    def get_summary_from_api(self, text: str) -> str:
        """Function where request to BART model transformers API occurs"""
        sum_length = len(text.split()) / 2
        min_length = 30
        if sum_length <= min_length:
            min_length = 1

        summary = self.model(
            text,
            max_length=sum_length,
            min_length=30,
            do_sample=False,
        )
        sum_text = summary[0]["summary_text"]
        return sum_text


class ChatGPT:
    model_name = "GPT"
    api_key = os.getenv("OPENAI_API_KEY")

    def get_summary_from_api(self, text: str) -> str:
        """Function where request to Chat GPT API occurs"""
        length = 500
        model_engine = "text-davinci-002"
        openai.api_key = self.api_key
        prompt = f"Summarize the following text in {length} words or fewer: " f"{text}"
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=length,
            n=1,
            stop=None,
            temperature=0.5,
        )
        summary = completions.choices[0].text

        return summary
