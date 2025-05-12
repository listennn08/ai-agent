from functools import reduce
from app.state import AgentState


def run_steps(step: callable, agent_state: AgentState, sid: str) -> AgentState:
    print(f"Running step: {step.__name__}")
    print(f"Agent state: {agent_state}")
    print("---")
    return step(sid, agent_state)


def process_message(sid: str, agent_state: AgentState, steps: list):
    return reduce(lambda state, step: run_steps(step, state, sid), steps, agent_state)
