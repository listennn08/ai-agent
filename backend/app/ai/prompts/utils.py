import logging
from langchain_core.prompts import PromptTemplate

from app.ai.prompts.persona import BARTENDER_PERSONA
from app.services.chat.chat_storage_base import IChatStorage
from app.services.user.basic import IUserPreferenceService
from app.state import AgentState


main_logger = logging.getLogger("sipp")


def build_llm_context(
    sid: str,
    agent_state: AgentState,
    chat_storage: IChatStorage,
    user_preference_service: IUserPreferenceService,
):
    # Retrieve history and preferences
    history = chat_storage.get_history(sid)
    user_pref = user_preference_service.get_user_preference(1)
    preferences = user_pref.preferences if user_pref else {}
    return {
        "history": history,
        "preferences": preferences,
        "user_input": agent_state.query[-1] if agent_state.query else "",
    }


def build_prompt(
    template: str,
    input_variables: list,
    format_instructions: str = "",
    persona: str = BARTENDER_PERSONA,
    partial_variables: dict = {},
) -> PromptTemplate:
    preferences_prompt = "User preferences: {preferences}"

    full_template = f"""
{persona.strip()}
{preferences_prompt}
{template.strip()}
"""

    prompt = PromptTemplate(
        template=full_template.strip(),
        input_variables=input_variables,
        partial_variables={
            **partial_variables,
            "format_instructions": format_instructions,
        },
    )

    return prompt
