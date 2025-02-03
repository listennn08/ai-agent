import json
import socketio

from api.generate import generate_drink
from models import UserInput


sio = socketio.AsyncServer(
  async_mode="asgi",
  cors_allowed_origins=[]
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
  user_input = UserInput(**json.loads(message))
  print("Received message: " + user_input.user_input)
  response = generate_drink(user_input)
  await sio.send(
    data=response.json(),
    room=sid
  )


@sio.event
async def custom_event(sid, message):
  print("Received custom event: " + message)