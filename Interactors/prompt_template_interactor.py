from typing import List
from langchain.prompts import PromptTemplate
from Interfaces.Interactor.prompt_template_interactor_interface import \
    PromptTemplateInteractorInterface


class PromptTemplateInteractor(PromptTemplateInteractorInterface):
    def get_prompt_template(self, prompt_template_text: str,
                            input_variables: List[str]):
        """
            Creates a PromptTemplate object from a provided template text and a list of input variables.

            Args:
                prompt_template_text (str): The text of the prompt template.
                input_variables (List[str]): A list of variable names that the prompt template expects.

            Returns:
                PromptTemplate: A PromptTemplate object representing the constructed prompt.

        """
        return PromptTemplate(template=prompt_template_text,
                              input_variables=input_variables,
                              template_format="f-string")
