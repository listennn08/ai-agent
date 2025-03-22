from pydantic import Field
from typing import TypedDict, List


class AgentState(TypedDict):
    query: List[str] = Field(description="The query of the user")
    messages: List[str] = Field(description="The message of the user")
    drinks: List[str] = Field(description="The drinks of the user")
    keywords: List[str] = Field(description="The keyword of the user")
    next: str = Field(description="The next step of the user")
