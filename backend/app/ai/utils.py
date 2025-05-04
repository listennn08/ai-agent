import json
import logging

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from ai.llm_service import LLMService
from schemas import BooleanModel

main_logger = logging.getLogger("sipp")


def check_user_input_is_follow_up(user_input: str, history: list) -> bool:
    """
    Check if the user's input is a follow up question
    """
    llm = LLMService().get_llm("gpt-4o-mini")

    template = """
    History: {history}
    User input: {user_input}

    According to the history, is user want to ask a follow up question/instruction?
    {format_instructions}
    """

    parser = PydanticOutputParser(pydantic_object=BooleanModel)

    prompt = PromptTemplate(
        template=template,
        input_variables=["user_input"],
        partial_variables={
            "history": history,
            "format_instructions": parser.get_format_instructions(),
        },
    )

    chain = prompt | llm | parser

    response = json.loads(chain.invoke({"user_input": user_input}).json())

    main_logger.info(f"Is follow up: {response.get('bool_value', False)}")

    return response.get("bool_value", False)
