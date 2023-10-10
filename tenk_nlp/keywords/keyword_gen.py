import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from loguru import logger


def run_keyword_generator(
    text: str,
    filter_stop_words: bool = True,
    number_of_kw: int = 20,
) -> list[tuple[str, int]]:
    """Wrapper to use to call word tokenizing logic"""

    logger.debug(f"Generating {number_of_kw} keywords from input text...")

    tokenized = tokenize_text(text, filter_stop_words=filter_stop_words)

    keywords = get_keywords_from_tokens(tokenized, number=number_of_kw)

    logger.debug(f"Keywords: {keywords}")

    return keywords


def tokenize_text(text: str, filter_stop_words: bool = False) -> list[str]:
    """
    Tokenizes a given text into a list of tokens.

    Args:
        text (str): The input text to tokenize.
        filter_stop_words (bool): whether or not to filter out stopwords

    Returns:
        list: A list of tokens.
    """
    tokens = word_tokenize(text)

    if filter_stop_words:
        # this creates a set of stopwords in english
        stop_words = set(stopwords.words("english"))
        stop_words.update(["may", "could", "also", "including", "can", "many"])
        # first filter out "stop words" or unwanted words
        filtered_words = []
        for word in tokens:
            # casefold makes it so the case doesn't matter
            if word.casefold() not in stop_words:
                filtered_words.append(word)

        # next filter out any punctuation
        words = [word.lower() for word in filtered_words if word.isalpha()]

    else:
        words = tokens

    return words


def get_keywords_from_tokens(
    word_tokens: list[str],
    number: int = 20,
) -> list[tuple[str, int]]:
    """
    Given a list of words from a body of text, creates a frequency distribution and extracts the top keywords by frequency.

    Args:
        word_tokens (list): list of wordss
        number (int): number of top keywords to extract

    Returns:
        list: A list of the top keywords as tuples containing the word and frequency of that word.

    """
    # Create a frequency distribution for the list of tokenized words
    fdist = nltk.probability.FreqDist(word_tokens)

    # this will look at the # given most common words - we can do more or less by giving this a lower or higher integer
    common_words = fdist.most_common(number)

    # TODO: stemming and lemmatization
    return common_words
