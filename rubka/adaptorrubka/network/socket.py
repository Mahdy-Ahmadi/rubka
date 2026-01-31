import sys
import subprocess

def install_and_import(package_name):
    try:
        __import__(package_name)
    except ModuleNotFoundError:
        print(f"Module '{package_name}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    finally:
        globals()[package_name] = __import__(package_name)

install_and_import("websocket")

from websocket import WebSocketApp

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
