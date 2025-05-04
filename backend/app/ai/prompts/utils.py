import logging
from langchain_core.prompts import PromptTemplate
from .persona import BARTENDER_PERSONA

main_logger = logging.getLogger("sipp")


def build_prompt(
    template: str,
    input_variables: list,
    format_instructions: str = "",
    persona: str = BARTENDER_PERSONA,
    partial_variables: dict = {},
) -> PromptTemplate:
    full_template = f"""{persona.strip()}\n{template.strip()}"""

    prompt = PromptTemplate(
        template=full_template,
        input_variables=input_variables,
        partial_variables={
            **partial_variables,
            "format_instructions": format_instructions,
        },
    )

    return prompt
