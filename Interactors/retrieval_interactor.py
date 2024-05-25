from typing import Any
from langchain.chains import RetrievalQA

from Interfaces.Interactor.retrieval_interactor_interface import \
    RetrievalQAInteractorInterface


class RetrievalQAInteractor(RetrievalQAInteractorInterface):
    def get_retrievalqa(self, retriever: Any,
                        prompt_template: Any,
                        llm: Any):
        """
          This function constructs a RetrievalQA object using a retriever, prompt template, and LLM.

          Args:
              retriever (Any): The retriever object to be used for retrieval.
              prompt_template (Any): The prompt template to be used for generating the final prompt.
              llm (Any): The large language model (LLM) to be used for generating the response.

          Returns:
              RetrievalQA: A RetrievalQA object.

          Raises:
               (Optional) Exceptions that may occur during the creation of the RetrievalQA object.
          """
        chain_type_kwargs = {"prompt": prompt_template}

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs=chain_type_kwargs,
            verbose=True
        )
