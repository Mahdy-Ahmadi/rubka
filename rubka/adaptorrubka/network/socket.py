
try:
    from websocket import WebSocketApp
except:
    import os
    try:
        os.system("pip install websocket-client")
    except:
        os.system("python -m pip install websocket-client")
from .helper import Helper
from json import dumps, loads
from threading import Thread
from ..types import Message
from ..exceptions import NotRegistered, TooRequests
from ..utils import Utils
from re import match
from time import sleep

class Socket:
    def __init__(self, methods) -> None:
        self.methods = methods
        self.handlers = {}

    ...