from pydantic import BaseModel, Field
from typing import List


class AgentState(BaseModel):
    query: List[str] = Field(description="The query of the user", default=[])
    drinks: List[str] = Field(description="The drinks of the user", default=[])
    keywords: List[str] = Field(description="The keyword of the user", default=[])
    anti_keywords: List[str] = Field(
        description="The anti-keyword of the user", default=[]
    )
    next: str = Field(description="The next step of the user", default="")
