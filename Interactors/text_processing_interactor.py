from typing import List

from Constants.profanity_words_constants import PROFANITY_WORD_LIST
from Constants.text_processing_constants import FRACTIONS, COMPOUND_WORDS
from Constants.validate_constants import ENGLISH_STOP_WORDS
from Interfaces.Interactor.text_preprocessing_interactor_interface import \
    TextProcessingInteractorInterface
import re


class TextProcessingInteractor(TextProcessingInteractorInterface):

    def remove_consecutive_repeating_words(self, text: str) -> str:
        """
        Removes consecutively repeating words from a string.

        Args:
            text (str): The input string.

        Returns:
            str: The string after removing consecutively repeating words.
        """
        cleaned_text = re.sub(r'\b(\w+)(?:\s+\1\b)+', r'\1', text)
        return cleaned_text

    def clean_text(self, text: str) -> str:
        """
            Cleans a text string by removing non-alphanumeric characters, converting to lowercase,
            and removing stop words.

            Args:
                text (str): The text string to be cleaned.

            Returns:
                str: The cleaned text string.
        """
        pattern = r'[^a-zA-Z0-9\s]'
        result = re.sub(pattern, '', text.lower())
        return " ".join(
            [word for word in result.split() if word not in ENGLISH_STOP_WORDS])

    def profanity_check(self, text: str) -> bool:
        """
           Checks a text string for profanity using a predefined list of profanity words.

           Args:
               text (str): The text string to be checked for profanity.

           Returns:
               bool: True if the text contains profanity, False otherwise.
        """
        input_text = self.clean_text(text)

        set1 = set(input_text.split())
        set2 = set(PROFANITY_WORD_LIST)

        intersection_set = set1.intersection(set2)

        print("PROFANITY WORDS: ", intersection_set)
        if intersection_set:
            return True
        else:
            return False

    def add_source_in_response_text(self,
                                    response_text: str,
                                    source_docs: List[str]) -> str:
        return response_text + "\n\nSource Documents: \n\t" + str(
            "\n".join(list(set(source_docs))))

    def handling_numerical_fractions(self, text: str) -> str:
        """
            Replaces numerical fractions in a text string with their corresponding representation
            from a predefined dictionary (if available) or returns the original fraction string.

            Args:
                text (str): The text string to be processed.

            Returns:
                str: The processed text string with numerical fractions potentially replaced.

        """
        fractions = FRACTIONS
        pattern = r'(\d+)/(\d+)'

        def repl(match):
            fraction = match.group(0)
            return fractions.get(fraction, fraction)

        return re.sub(pattern, repl, text)

    def text_post_processing(self, text: str, source_docs: List[str]) -> str:

        text = self.remove_consecutive_repeating_words(text)
        """
            Performs post-processing on a text string by removing potential prefixes like "Question:",
            "Context:", or "Note:".

            Args:
                text (str): The text string to be processed.

            Returns:
                str: The processed text string with potential prefixes removed.

            Raises:
                (Optional) AttributeError: If the regular expression search (`re.search`) doesn't find a match,
                    indicating the text might not have the expected prefixes. This exception can be handled
                    according to your specific needs (e.g., returning the original text or logging a warning).
            """
        try:
            pattern = r"(?is)(Question: |Context: |Note: )"
            match = re.search(pattern, text)
            clipped_text = text[match.end():]

        except AttributeError:
            clipped_text = text

        final_text = self.add_source_in_response_text(
            response_text=clipped_text,
            source_docs=source_docs)

        return final_text

    def special_token_remover(self, text: str) -> str:
        """
        Removes special tokens of the form <<TOKEN>> or <<OPTIONAL>> from the given text.

        Args:
            text (str): The input text containing special tokens.

        Returns:
            str: The text with special tokens removed.

        Raises:
            TypeError: If the input text is not a string.
        """
        try:
            pattern = r'<<(?:[A-Za-z])>>'
            cleaned_text = re.sub(pattern, '', text)
            return cleaned_text
        except re.error:
            return text

    def create_compound_words(self, text: str) -> str:
        """
        Inserts hyphens into a string to convert words like "punchin" into "punch-in".

        Args:
            text (str): The input string.

        Returns:
            str: The string with hyphens inserted.
        """
        word_mappings = COMPOUND_WORDS

        try:
            for word, hyphenated_word in word_mappings.items():
                text = text.replace(word, hyphenated_word)
            return text
        except Exception as e:
            return text

    def perform_text_processing(self, text: str) -> str:
        text = self.handling_numerical_fractions(text=text)
        text = self.create_compound_words(text=text)
        text = self.special_token_remover(text=text)
        return text
