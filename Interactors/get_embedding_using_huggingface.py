from langchain_community.embeddings import HuggingFaceEmbeddings

from Constants.embedding_config_constants import MODEL_NAME, MODEL_KWARGS, \
    ENCODE_KWARGS
from Interfaces.Interactor.get_embedding_using_huggingface_interface import \
    HuggingfaceEmbeddingsInteractorInterface


class HuggingfaceEmbeddingsInteractor(HuggingfaceEmbeddingsInteractorInterface):
    def get_embeddings_object(self):
        return HuggingFaceEmbeddings(
            model_name=MODEL_NAME,
            model_kwargs=MODEL_KWARGS,
            encode_kwargs=ENCODE_KWARGS
        )
