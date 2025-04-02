import socketio
import json
from db import get_db
from depends import (
    get_drink_photo_repository,
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


agent_state = {
    "query": [],
    "messages": [],
    "keywords": [],
    "drinks": [],
}


@sio.event
async def message(sid, message):
    try:
        global agent_state
        # history = get_chat_history()
        llm_service = get_llm_service()
        vector_store = get_vector_store(llm_service)
        drink_photo_repository = get_drink_photo_repository(get_db())
        drink_service = get_drink_service(
            vector_store, llm_service, drink_photo_repository
        )

        user_input = UserInput(**json.loads(message))

        agent_state["query"].append(user_input.user_input)
        keywordsResp = drink_service.extract_keywords(agent_state)
        agent_state["keywords"] = keywordsResp["keywords"]
        agent_state["messages"] = keywordsResp["messages"]

        print("extract keywords", agent_state["keywords"])

        if len(agent_state["keywords"]) < 3:
            resp = drink_service.verify_user_input_and_get_clarification(agent_state)

            agent_state["messages"] = resp["messages"]
            agent_state["keywords"] = resp["keywords"]
            agent_state["drinks"] = resp["drinks"]

            print("verify user input and get clarification", agent_state["keywords"])

            return await sio.emit(
                event="message",
                data={"message": agent_state["messages"][-1]},
                room=sid,
            )

        drinksResp = drink_service.retrieve(agent_state)
        agent_state["drinks"] = drinksResp["drinks"]
        agent_state["messages"] = drinksResp["messages"]

        if len(agent_state["drinks"]) > 0:
            [drink] = agent_state["drinks"]
            print(drink)
            return await sio.emit(
                event="message",
                data={
                    "message": agent_state["messages"][-1],
                    "drinks": {
                        "name": drink.name,
                        "photo": drink_service.get_drink_photo(drink.sku),
                    },
                },
                room=sid,
            )

        agent_state["keywords"] = []
        agent_state["drinks"] = []
        agent_state["messages"].append(
            "I'm sorry, I don't have any drinks that match your preferences."
        )
        await sio.emit(
            event="message",
            data={"message": agent_state["messages"][-1]},
            room=sid,
        )
    finally:
        print("================")
        print("query", "\n\t".join(agent_state["query"]))
        print("messages", "\n\t".join(agent_state["messages"]))
        print("keywords", "\n\t".join(agent_state["keywords"]))
        print("drinks", "\n\t".join(map(lambda x: x.name, agent_state["drinks"])))
        print("================")


@sio.event
async def custom_event(sid, message):
    print("Received custom event: " + message)
