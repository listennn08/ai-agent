import json
import socketio
from langchain_core.messages import trim_messages

from depends import (
    get_drink_service,
    get_vector_store,
    get_llm_service,
    get_chat_history,
)
from schemas import UserInput
from ai.utils import check_user_input_is_follow_up

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path="/socket.io")


@sio.event
async def connect(sid, environ):
    await sio.emit(
        event="welcome", data={"message": "Welcome to the server!"}, room=sid
    )
    print("Connected: " + sid)


@sio.event
async def disconnect(sid):
    print("Disconnected: " + sid)


@sio.event
async def message(sid, message):
    history = get_chat_history()
    llm_service = get_llm_service()
    vector_store = get_vector_store(llm_service)
    drink_service = get_drink_service(vector_store, llm_service)

    user_input = UserInput(**json.loads(message))

    history.add_human_message(user_input.user_input)
    print("Received message: " + user_input.user_input)

    await sio.emit(event="loading", data={"message": "Retrieving drinks..."}, room=sid)

    drinks = []
    new_drink = None
    selected_history = history.get_history()

    try:
        if check_user_input_is_follow_up(user_input, selected_history):
            trim_messages(
                messages=selected_history,
                token_counter=len,
                max_tokens=5,
                strategy="last",
                start_on="human",
                include_system=True,
                allow_partial=False,
            )
        else:
            drinks = drink_service.retrieve(user_input.user_input)
    except Exception as e:
        print(e)
        await sio.emit(
            event="error", data={"message": "Error retrieving drinks"}, room=sid
        )
        return

    try:
        await sio.emit(
            event="loading", data={"message": "Generating new drink..."}, room=sid
        )
        new_drink = drink_service.generate(
            user_input.user_input, drinks, selected_history
        )

        history.add_ai_message(new_drink.json())
    except Exception as e:
        print(e)
        await sio.emit(
            event="error", data={"message": "Error generating new drink"}, room=sid
        )
        return

    await sio.emit(
        event="new_drink", data={"data": json.loads(new_drink.json())}, room=sid
    )


@sio.event
async def custom_event(sid, message):
    print("Received custom event: " + message)
