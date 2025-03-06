import json
import socketio

from api.v1.generate import generate_drink
from depends import get_drink_retrieve_service, get_vector_store, get_llm_service
from schemas import UserInput


sio = socketio.AsyncServer(
  async_mode="asgi",
  cors_allowed_origins="*"
)
sio_app = socketio.ASGIApp(
  socketio_server=sio,
  socketio_path="/socket.io"
)


@sio.event
async def connect(sid, environ):
  print("Connected: " + sid)


@sio.event
async def disconnect(sid):
  print("Disconnected: " + sid)


@sio.event
async def message(sid, message):
  llm_service = get_llm_service()
  vector_store = get_vector_store(llm_service)
  drink_retrieve_service = get_drink_retrieve_service(vector_store)
  user_input = UserInput(**json.loads(message))
  print("Received message: " + user_input.user_input)
  response = generate_drink(user_input, drink_retrieve_service)
  await sio.send(
    data=response.json(),
    room=sid
  )


@sio.event
async def custom_event(sid, message):
  print("Received custom event: " + message)
