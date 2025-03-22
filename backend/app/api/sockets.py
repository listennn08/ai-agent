import socketio
import json
from depends import (
    get_drink_service,
    get_vector_store,
    get_llm_service,
    # get_chat_history,
)
from schemas import UserInput

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path="/socket.io")


@sio.event
async def connect(sid, environ):
    # history = get_chat_history()
    # llm_service = get_llm_service()
    # vector_store = get_vector_store(llm_service)
    # drink_service = get_drink_service(vector_store, llm_service)
    # message = drink_service.generate_welcome_message(history.get_history())

    await sio.emit(
        event="welcome",
        data={
            # "message": message
            "message": "🍹 Welcome! I'm your exclusive bartender, please tell me your preferences, I will recommend the perfect drink for you!"
        },
        room=sid,
    )
    print("Connected: " + sid)


@sio.event
async def disconnect(sid):
    print("Disconnected: " + sid)


keywords = []


@sio.event
async def message(sid, message):
    # history = get_chat_history()
    llm_service = get_llm_service()
    vector_store = get_vector_store(llm_service)
    drink_service = get_drink_service(vector_store, llm_service)

    user_input = UserInput(**json.loads(message))

    agent_state = {
        "query": [user_input.user_input],
        "messages": [],
        "drinks": [],
        "keywords": [],
    }

    agent_state = drink_service.extract_keywords(agent_state)
    keywords = agent_state["keywords"]

    print("================")
    print("query", ", ".join(agent_state["query"]))
    print("messages", ", ".join(agent_state["messages"]))
    print("keywords", ", ".join(keywords))
    print("drinks", ", ".join(agent_state["drinks"]))
    print("================")

    if len(keywords) < 3:
        agent_state = drink_service.verify_user_input_and_get_clarification(agent_state)
        return await sio.emit(
            event="message",
            data={"message": agent_state["messages"][-1]},
            room=sid,
        )

    agent_state = drink_service.retrieve(agent_state)

    if len(agent_state["drinks"]) > 0:
        await sio.emit(
            event="message",
            data={
                "message": agent_state["messages"][-1],
                "drinks": list(map(lambda x: x.json(), agent_state["drinks"])),
            },
            room=sid,
        )
    else:
        await sio.emit(
            event="message",
            data={
                "message": "I'm sorry, I don't have any drinks that match your preferences."
            },
            room=sid,
        )


@sio.event
async def custom_event(sid, message):
    print("Received custom event: " + message)
