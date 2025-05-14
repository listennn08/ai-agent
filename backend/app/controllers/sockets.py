from langchain_core.messages import AIMessage, HumanMessage
import socketio
import logging
import json
from typing import Dict
from app.db import get_db
from app.depends import (
    get_drink_photo_repository,
    get_drink_service,
    get_vector_store,
    get_llm_service,
    get_chat_history,
    get_user_preference_service,
)
from app.schemas import UserInput
from app.utils import process_message
from app.state import AgentState

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path="/socket.io")

main_logger = logging.getLogger("sipp")


# Initialize services
chat_storage = get_chat_history()
llm_service = get_llm_service()
vector_store = get_vector_store(llm_service)
db_session = next(get_db())
drink_photo_repository = get_drink_photo_repository(db_session)
user_preference_service = get_user_preference_service(db_session)
drink_service = get_drink_service(
    vector_store=vector_store.vector_store,
    llm_service=llm_service,
    drink_photo_repository=drink_photo_repository,
    chat_storage=chat_storage,
    user_preference_service=user_preference_service,
)


# Initialize agent state
user_states: Dict[str, AgentState] = {}


@sio.event
async def connect(sid, environ, auth):
    # check token
    token = auth.get("token")
    main_logger.info(f"token: {token}")
    if not token:
        await sio.emit(
            event="error",
            data={"message": "Unauthorized"},
            room=sid,
        )
        await sio.disconnect(sid)
        return

    main_logger.info("Connected: " + sid)


@sio.event
async def init(sid):
    chat_storage.init_user(sid)
    user_states[sid] = AgentState()

    message = drink_service.generate_welcome_message(sid, user_states[sid])
    chat_storage.append_message(sid, AIMessage(message))
    await sio.emit(
        event="welcome",
        data={"message": message},
        room=sid,
    )


@sio.event
async def disconnect(sid):
    main_logger.info("Disconnected: " + sid)
    chat_storage.clear(sid)
    user_states.pop(sid, None)


@sio.event
async def message(sid: str, message: str):
    try:
        agent_state = user_states.get(sid)

        user_input = UserInput(**json.loads(message))
        agent_state.query.append(user_input.user_input)
        chat_storage.append_message(sid, HumanMessage(user_input.user_input))

        steps = [
            drink_service.extract_keywords
            if len(agent_state.keywords) < 3
            else lambda sid, x: x,
            drink_service.verify_user_input_and_get_clarification
            if len(agent_state.keywords) < 3
            else lambda sid, x: x,
            user_preference_service.create_or_update_user_preference,
            drink_service.retrieve
            if len(agent_state.keywords) >= 3
            else lambda sid, x: x,
        ]
        agent_state = process_message(sid, agent_state, steps)
        history = chat_storage.get_history(sid)
        main_logger.debug(f"history {history}")

        drink = agent_state.drinks[0] if len(agent_state.drinks) > 0 else None

        photo = None
        if drink:
            photo = drink_service.get_drink_photo(drink.sku)

        response = {
            "message": history[-1]["message"] if history else None,
            "drinks": {
                **(drink.model_dump()),
                "photo": photo,
            }
            if drink
            else None,
        }
        await sio.emit(
            event="message",
            data=response,
            room=sid,
        )

    except Exception as e:
        main_logger.error(e)
        await sio.emit(
            event="error",
            data={"message": str(e)},
            room=sid,
        )


@sio.event
async def custom_event(sid, message):
    main_logger.info(f"Received custom event: {message}")
