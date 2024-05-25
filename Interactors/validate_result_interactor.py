from sentence_transformers import SentenceTransformer, util
from Constants.embedding_config_constants import MODEL_NAME
from Constants.validate_constants import SIMILARITY_THRESHOLD
from Interactors.text_processing_interactor import TextProcessingInteractor
from Interfaces.Interactor.validate_result_interactor_interface import \
    ValidateResultsInteractorInterface


class ValidateResultsInteractor(ValidateResultsInteractorInterface):

    def validate_commonality(self, input_text: str, search_result: str) -> bool:
        """
            Validates whether there's a commonality between two text strings based on shared words.

             Args:
                input_text (str): The first text string to compare.
                search_result (str): The second text string to compare.

            Returns:
                bool: True if the two text strings have at least one common word, False otherwise.

        """
        text_processing_interactor = TextProcessingInteractor()

        input_text = text_processing_interactor.clean_text(input_text)
        search_result = text_processing_interactor.clean_text(search_result)

        set1 = set(input_text.split())
        set2 = set(search_result.split())

        print("Query : ", set1)
        print("CHUNK : ", set2)

        intersection_set = set1.intersection(set2)

        print("COMMON : ", intersection_set)

        if (len(input_text) > 1
                and len(search_result) > 1
                and len(intersection_set) >= 1):
            if intersection_set:
                return True
            else:
                return False
        else:
            return False

    def validate_results(self, search_result: str, input_text: str) -> bool:
        """
            Validates the similarity between a search result and the input text using a combination of
            sentence embeddings and word-level commonality checks.

            Args:
                search_result (str): The search result string to validate.
                input_text (str): The original input text string.

            Returns:
                bool: True if the search result is considered valid (sufficiently similar to the input text),
                False otherwise.

        """
        model = SentenceTransformer(model_name_or_path=MODEL_NAME)
        embeddings = model.encode([search_result, input_text],
                                  convert_to_tensor=True)
        cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        similarity_score = cosine_sim.item()

        print("SCORE: ", similarity_score)

        is_common = self.validate_commonality(input_text=input_text,
                                              search_result=search_result)

        if is_common:
            if similarity_score >= SIMILARITY_THRESHOLD:
                return True
            else:
                return False
        else:
            return False
