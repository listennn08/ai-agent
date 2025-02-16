
from fastapi import Request


def get_drink_retrieve_service(req: Request):
    return req.app.state.drink_retrieve_service