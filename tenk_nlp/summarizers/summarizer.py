# base class that other nlp model classes will inherit from
import time
from tenk_nlp.keywords.keyword_gen import tokenize_text

from loguru import logger


class Summarizer:
    def __init__(self, model) -> None:
        self.model = model

    def summarize_recursive(self, text: str, max_tokens: int) -> str:
        """
        Recursively summarizes text and combines the summaries until the resulting text
        contains fewer than max_tokens tokens.

        Args:
            text (str): The input text to summarize recursively.
            max_tokens (int): The maximum number of tokens for the final summary.

        Returns:
            str: The summarized text.
        """
        if len(tokenize_text(text)) <= max_tokens:
            # If the input text is already below the max_tokens limit, no further summarization is needed.
            return text

        # Break the input text into sections
        sections = self.break_text_into_sections(text, max_tokens)
        logger.debug(f"Text broken up into {len(sections)} sections for summarization")

        # Summarize each section and combine the summaries
        summarized_sections = [self.summarize_text(section) for section in sections]

        # Recursively call summarize_recursive on the combined summaries
        combined_sections = " ".join(summarized_sections)
        logger.debug(
            f"Summarized sections joined together, new length: {len(combined_sections)}"
        )
        combined_summary = self.summarize_recursive(combined_sections, max_tokens)

        return combined_summary

    def break_text_into_sections(
        self,
        input_text: str,
        max_tokens: int = 850,
    ) -> list[str]:
        """
        Breaks down text into sections of a specified maximum number of tokens.

        Args:
            text (str): The input text to break into sections.
            max_tokens (int): The maximum number of tokens per section.

        Returns:
            list: A list of text sections, each containing at most max_tokens tokens.
        """

        tokens = tokenize_text(input_text)
        sections = []
        current_section = []

        for token in tokens:
            if len(current_section) + len(token) <= max_tokens:
                current_section.append(token)
            else:
                sections.append(" ".join(current_section))
                current_section = [token]

        # Add any remaining tokens as the last section
        if current_section:
            sections.append(" ".join(current_section))

        return sections

    def summarize_text(self, text: str) -> str:
        """
        Calls the text summarization function for the given model

        Args:
            text (str): The input text to summarize.

        Returns:
            str: The summarized text.
        """
        tic = time.perf_counter()
        logger.info(
            f"Summarizing with {self.model.model_name} model, initial text length = {len(text)}"
        )
        # set desired summary max length to half the initial length
        logger.debug(f"Original text: {text}")
        summary = self.model.get_summary_from_api(text)
        toc = time.perf_counter()
        time_diff = toc - tic
        logger.debug(f"Summarized text: {summary}")
        logger.info(
            f"Summarized text in {time_diff:0.4f} seconds, new length = {len(summary)}"
        )
        return summary
