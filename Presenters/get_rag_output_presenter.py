import os
from typing import Tuple, Optional, List
from Constants.prompt_constants import INPUT_VARIABLES, PROMPT_TEXT
from Constants.retriever_constants import TOP_RESULTS, SEARCH_TYPE
from Constants.return_constants import RELEVANT_QUERY, NO_CODE, \
    PROFANITY_RESPONSE, POLITE_REFUSAL
from Firewall.malicious_text_firewall import SecurityFirewall
from Interactors.text_processing_interactor import \
    TextProcessingInteractor
from Interactors.vector_stores_interactor import \
    VectorStoresInteractor
from Interactors.get_embedding_using_huggingface import \
    HuggingfaceEmbeddingsInteractor
from Interactors.load_llm_interactor import LoadLLMInteractor
from Interactors.prompt_template_interactor import PromptTemplateInteractor
from Interactors.retrieval_interactor import RetrievalQAInteractor
from Interactors.validate_result_interactor import ValidateResultsInteractor
from Interfaces.Presenter.get_rag_output_presenter_interface import \
    GetRAGOutputPresenterInterface
from rich.console import Console

console = Console()


class GetRAGOutputPresenter(GetRAGOutputPresenterInterface):

    def __init__(
            self,
            firewall: SecurityFirewall,
            text_processing_interactor: TextProcessingInteractor,
            huggingface_embeddings_interactor: HuggingfaceEmbeddingsInteractor,
            retriever_interactor: RetrievalQAInteractor,
            chroma_vector_store_interactor: VectorStoresInteractor,
            load_local_llm_interactor: LoadLLMInteractor,
            prompt_template_interactor: PromptTemplateInteractor,
            validate_text_interactor: ValidateResultsInteractor):

        self.firewall = firewall
        self.text_processing_interactor = text_processing_interactor
        self.huggingface_embeddings_interactor = huggingface_embeddings_interactor
        self.retriever_interactor = retriever_interactor
        self.chroma_vector_store_interactor = chroma_vector_store_interactor
        self.load_local_llm_interactor = load_local_llm_interactor
        self.prompt_template_interactor = prompt_template_interactor
        self.validate_text_interactor = validate_text_interactor

    def get_output(self, input_query: str) -> Optional[Tuple[str, List[str]]]:
        profanity_exists = \
            self.text_processing_interactor.profanity_check(text=input_query)
        if profanity_exists:
            return PROFANITY_RESPONSE

        print("\t Checking Malicious code\t")
        if self.firewall.check_malicious_code_input(prompt_text=input_query):
            return NO_CODE
        print("\t Checking Malicious prompt\t")
        if self.firewall.check_malicious_string(prompt_text=input_query):
            return POLITE_REFUSAL

        print("\t Performing text processing\t")
        input_query = \
            self.text_processing_interactor.perform_text_processing(
                text=input_query)

        print("\t Loading LLM\t")
        local_llm = self.load_local_llm_interactor.load_llm_model(
            local_llm_path=os.path.abspath(
                './../LocalLLM/zephyr-7b-beta.Q5_K_S.gguf'))

        embeddings = (self.huggingface_embeddings_interactor
                      .get_embeddings_object())
        print("\t Getting Embedding Object\t")

        print("\t Loading Chroma DB\t")
        chroma_vector_store = (
            self.chroma_vector_store_interactor.load_vector_stores(
                embedding_function=embeddings,
                file_path=os.path.abspath(
                    './../Persist_Directory/document_cosine')
            ))

        retriever = chroma_vector_store.as_retriever(
            search_kwargs=TOP_RESULTS,
            search_type=SEARCH_TYPE
        )

        print("\t Getting Prompt Template\t")
        prompt_template = self.prompt_template_interactor.get_prompt_template(
            prompt_template_text=PROMPT_TEXT,
            input_variables=INPUT_VARIABLES
        )
        print("\t Getting Chunks\t")
        semantic_search = retriever.get_relevant_documents(input_query)
        retrieved_chunks = \
            "\n\n[SEPARATOR]\n\n".join([res.page_content for res in
                                        semantic_search])
        source_docs = [res.metadata['source'] for res in semantic_search]
        console.print("SIMILAR CHUNK : " +
                      '\x1b[38;2;255;165;0m' +
                      str(retrieved_chunks) +
                      '\x1b[0m')

        console.print(
            "SOURCE: " +
            '\x1b[38;2;0;100;255m' +
            str(source_docs) + '\x1b[' '0m')

        try:
            is_valid_query = self.validate_text_interactor.validate_results(
                search_result=retrieved_chunks,
                input_text=input_query)
            if not is_valid_query:
                return RELEVANT_QUERY
        except IndexError:
            return RELEVANT_QUERY

        qa_retrieval = self.retriever_interactor.get_retrievalqa(
            retriever=retriever,
            llm=local_llm,
            prompt_template=prompt_template
        )

        bot_response = qa_retrieval.invoke(input_query)
        bot_result = bot_response['result']

        bot_response_processed = (
            self.text_processing_interactor.text_post_processing(
                text=bot_result,
                source_docs=source_docs))

        console.print(
            '\x1b[38;2;0;255;0m' + str(bot_response_processed) + '\x1b[0m')

        return bot_response_processed, source_docs
