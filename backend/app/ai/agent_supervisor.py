from typing import TypedDict


class AgentState(TypedDict):
    query: str
    agent_choice: str
    response: str


class AgentSupervisor:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AgentSupervisor, cls).__new__(cls)

        return cls.__instance

    def get_agent_response(self, query: str) -> AgentState:
        pass

    def get_agent_choice(self, query: str) -> str:
        pass
