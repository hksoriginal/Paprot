from langchain_community.llms import CTransformers

from Constants.transformers_constants import MODEL_TYPE, LIB, CONFIG
from Interfaces.Interactor.load_llm_interactor_interface import \
    LoadLLMInteractorInterface


class LoadLLMInteractor(LoadLLMInteractorInterface):
    def load_llm_model(self,
                       local_llm_path: str):
        """
            Loads a large language model (LLM) from a specified local path.

            Args:
                local_llm_path (str): The path to the directory containing the LLM model files.

            Returns:
                CTransformers: An instance of the CTransformers class representing the loaded LLM.

        """
        return CTransformers(
            model=local_llm_path,
            model_type=MODEL_TYPE,
            lib=LIB,
            **CONFIG
        )
