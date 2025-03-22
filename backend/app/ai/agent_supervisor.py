from state import AgentState


class AgentSupervisor:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AgentSupervisor, cls).__new__(cls)

        return cls.__instance

    def get_agent_response(self, state: AgentState) -> AgentState:
        pass

    def get_agent_choice(self, state: AgentState) -> AgentState:
        print(state)

        if state.get("drinks") and len(state.get("drinks")) > 0:
            return {
                "query": state.get("query") or [],
                "messages": state.get("messages") or [],
                "drinks": state.get("drinks") or [],
                "keywords": [],
                "next": "done",
            }
        elif not state.get("drinks") or len(state.get("drinks")) == 0:
            return {
                "query": state.get("query") or [],
                "messages": state.get("messages") or [],
                "drinks": [],
                "keywords": [],
                "next": "recollect",
            }

        if not state.get("keywords") or len(state.get("keywords")) < 3:
            return {
                "query": state.get("query") or [],
                "messages": state.get("messages") or [],
                "keywords": state.get("keywords") or [],
                "next": "clarify",
            }
        else:
            return {
                "query": state.get("query") or [],
                "messages": state.get("messages") or [],
                "drinks": state.get("drinks") or [],
                "keywords": state.get("keywords") or [],
                "next": "retrieve",
            }
