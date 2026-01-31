import requests
from typing import List, Optional, Dict, Any, Literal
from .exceptions import APIRequestError
from .adaptorrubka import Client as Client_get
from .logger import logger
from . import filters
from . import helpers
from typing import Callable
from .context import Message,InlineMessage
from typing import Optional, Union, Literal, Dict, Any
from pathlib import Path
import time
import datetime
import tempfile
from tqdm import tqdm
import os
API_URL = "https://botapi.rubika.ir/v3"
import mimetypes
import re
import sys
import subprocess
class InvalidTokenError(Exception):pass
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:return False

def get_importlib_metadata():
    try:
        from importlib.metadata import version, PackageNotFoundError
        return version, PackageNotFoundError
    except ImportError:
        if install_package("importlib-metadata"):
            try:
                from importlib_metadata import version, PackageNotFoundError
                return version, PackageNotFoundError
            except ImportError:
                return None, None
        return None, None

version, PackageNotFoundError = get_importlib_metadata()
def get_installed_version(package_name: str) -> str:
    if version is None:return "unknown"
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None
def get_latest_version(package_name: str) -> str:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data["info"]["version"]
    except Exception:return None


def show_last_six_words(text):
    text = text.strip()
    return text[-6:]
import requests
from pathlib import Path
from typing import Union, Optional, Dict, Any, Literal
import tempfile
import os
import requests
from typing import Any, Dict, List, Optional


class Robot:
    """
    Main class to interact with Rubika Bot API.
    Initialized with bot token.
    """

    def __init__(self, token: str, session_name: Optional[str] = None, auth: Optional[str] = None, Key: Optional[str] = None,
                 platform: str = "web", web_hook: Optional[str] = None, timeout: int = 10, show_progress: bool = False):
        """
        Initializes the Rubika bot with the provided token and configuration.

        Parameters:
            token (str): Bot token for authentication with the Rubika Bot API.
            session_name (str, optional): Name of the session for client identification. Defaults to None.
            auth (str, optional): Additional authentication value for custom client connection. Defaults to None.
            Key (str, optional): Encryption or verification key if required. Defaults to None.
            platform (str, optional): The platform for execution ("web", "android", etc.). Defaults to "web".
            web_hook (str, optional): URL for the webhook. Defaults to None.
            timeout (int, optional): Timeout duration for HTTP requests in seconds. Defaults to 10.
            show_progress (bool, optional): Flag to show progress. Defaults to False.

        Example:
            >>> bot = Robot(token="BOT_TOKEN", platform="android", timeout=15)
        """
        self.token = token
        self.timeout = timeout
        self.auth = auth
        self.show_progress = show_progress
        self.session_name = session_name
        self.Key = Key
        self.platform = platform
        self.web_hook = web_hook
        self.hook = web_hook
        self._offset_id = None
        self.session = requests.Session()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._callback_handlers: List[dict] = []
        self._message_handlers: List[dict] = []
        self._inline_query_handlers: List[dict] = []
        
        # Initialize the token
        self.geteToken()

        # Handle webhook setup
        if web_hook:
            self._set_webhook(web_hook)

    def _set_webhook(self, web_hook: str):
        """
        Sets the webhook URL and updates the bot endpoints.

        Parameters:
            web_hook (str): The URL of the webhook to be set.
        """
        try:
            json_url = requests.get(web_hook, timeout=self.timeout).json().get('url', web_hook)
            for endpoint_type in [
                "ReceiveUpdate",
                "ReceiveInlineMessage",
                "ReceiveQuery",
                "GetSelectionItem",
                "SearchSelectionItems"
            ]:
                print(self.update_bot_endpoint(self.web_hook, endpoint_type))
            self.web_hook = json_url
        except Exception as e:
            logger.error(f"Failed to set webhook from {web_hook}: {e}")
    
    def geteToken(self):
        """
        Retrieves the token for the bot.
        Implement the method as required.
        """
        pass

    def update_bot_endpoint(self, webhook: str, endpoint_type: str) -> str:
        """
        Updates the bot's endpoint.

        Parameters:
            webhook (str): The webhook URL.
            endpoint_type (str): The type of endpoint to update.

        Returns:
            str: The updated endpoint URL.
        """
        # Placeholder for actual endpoint update logic
        return f"{webhook}/{endpoint_type}"


    def _post(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a POST request to the Rubika Bot API.

        Parameters:
            method (str): The API method to call.
            data (dict): The data to send in the request.

        Returns:
            dict: The response from the API.

        Raises:
            APIRequestError: If the API request fails or the response is invalid.
        """
        url = f"{API_URL}/{self.token}/{method}"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            try:
                json_resp = response.json()
            except ValueError:
                logger.error(f"Invalid JSON response from {method}: {response.text}")
                raise APIRequestError(f"Invalid JSON response: {response.text}")
            
            if method != "getUpdates":
                logger.debug(f"API Response from {method}: {json_resp}")
                
            return json_resp
        except requests.RequestException as e:
            logger.error(f"API request failed for method {method}: {e}")
            raise APIRequestError(f"API request failed for {method}: {e}") from e

    def get_me(self) -> Dict[str, Any]:
        """Get info about the bot itself."""
        return self._post("getMe", {})

    def geteToken(self):
        """Check if the bot token is valid by calling the `getMe` method."""
        response = self.get_me()
        if response.get('status') != "OK":
            raise InvalidTokenError("The provided bot token is invalid or expired.")
    def on_message_private(
        self,
        chat_id: Optional[Union[str, List[str]]] = None,
        commands: Optional[List[str]] = None,
        filters: Optional[Callable[[Message], bool]] = None,
        sender_id: Optional[Union[str, List[str]]] = None,
        sender_type: Optional[str] = None,  
        allow_forwarded: bool = True,
        allow_files: bool = True,
        allow_stickers: bool = True,
        allow_polls: bool = True,
        allow_contacts: bool = True,
        allow_locations: bool = True,
        min_text_length: Optional[int] = None,
        max_text_length: Optional[int] = None,
        contains: Optional[str] = None,
        startswith: Optional[str] = None,
        endswith: Optional[str] = None,
        case_sensitive: bool = False
    ):
        """
        Sync decorator for handling only private messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                
                if not message.is_private:
                    return

                
                if chat_id:
                    if isinstance(chat_id, str) and message.chat_id != chat_id:
                        return
                    if isinstance(chat_id, list) and message.chat_id not in chat_id:
                        return

                
                if sender_id:
                    if isinstance(sender_id, str) and message.sender_id != sender_id:
                        return
                    if isinstance(sender_id, list) and message.sender_id not in sender_id:
                        return

                
                if sender_type and message.sender_type != sender_type:
                    return

                
                if not allow_forwarded and message.forwarded_from:
                    return

                
                if not allow_files and message.file:
                    return
                if not allow_stickers and message.sticker:
                    return
                if not allow_polls and message.poll:
                    return
                if not allow_contacts and message.contact_message:
                    return
                if not allow_locations and (message.location or message.live_location):
                    return

                
                if message.text:
                    text = message.text if case_sensitive else message.text.lower()
                    if min_text_length and len(message.text) < min_text_length:
                        return
                    if max_text_length and len(message.text) > max_text_length:
                        return
                    if contains and (contains if case_sensitive else contains.lower()) not in text:
                        return
                    if startswith and not text.startswith(startswith if case_sensitive else startswith.lower()):
                        return
                    if endswith and not text.endswith(endswith if case_sensitive else endswith.lower()):
                        return

                
                if commands:
                    if not message.text:
                        return
                    parts = message.text.strip().split()
                    cmd = parts[0].lstrip("/")
                    if cmd not in commands:
                        return
                    message.args = parts[1:]

                
                if filters and not filters(message):
                    return

                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "commands": commands,
                "chat_id": chat_id,
                "private_only": True,
                "sender_id": sender_id,
                "sender_type": sender_type
            })
            return wrapper

        return decorator
    def on_message_channel(
        self,
        chat_id: Optional[Union[str, List[str]]] = None,
        commands: Optional[List[str]] = None,
        filters: Optional[Callable[[Message], bool]] = None,
        sender_id: Optional[Union[str, List[str]]] = None,
        sender_type: Optional[str] = None,  
        allow_forwarded: bool = True,
        allow_files: bool = True,
        allow_stickers: bool = True,
        allow_polls: bool = True,
        allow_contacts: bool = True,
        allow_locations: bool = True,
        min_text_length: Optional[int] = None,
        max_text_length: Optional[int] = None,
        contains: Optional[str] = None,
        startswith: Optional[str] = None,
        endswith: Optional[str] = None,
        case_sensitive: bool = False
    ):
        """
        Sync decorator for handling only private messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                
                if not message.is_channel:
                    return

                
                if chat_id:
                    if isinstance(chat_id, str) and message.chat_id != chat_id:
                        return
                    if isinstance(chat_id, list) and message.chat_id not in chat_id:
                        return

                
                if sender_id:
                    if isinstance(sender_id, str) and message.sender_id != sender_id:
                        return
                    if isinstance(sender_id, list) and message.sender_id not in sender_id:
                        return

                
                if sender_type and message.sender_type != sender_type:
                    return

                
                if not allow_forwarded and message.forwarded_from:
                    return

                
                if not allow_files and message.file:
                    return
                if not allow_stickers and message.sticker:
                    return
                if not allow_polls and message.poll:
                    return
                if not allow_contacts and message.contact_message:
                    return
                if not allow_locations and (message.location or message.live_location):
                    return

                
                if message.text:
                    text = message.text if case_sensitive else message.text.lower()
                    if min_text_length and len(message.text) < min_text_length:
                        return
                    if max_text_length and len(message.text) > max_text_length:
                        return
                    if contains and (contains if case_sensitive else contains.lower()) not in text:
                        return
                    if startswith and not text.startswith(startswith if case_sensitive else startswith.lower()):
                        return
                    if endswith and not text.endswith(endswith if case_sensitive else endswith.lower()):
                        return

                
                if commands:
                    if not message.text:
                        return
                    parts = message.text.strip().split()
                    cmd = parts[0].lstrip("/")
                    if cmd not in commands:
                        return
                    message.args = parts[1:]

                
                if filters and not filters(message):
                    return

                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "commands": commands,
                "chat_id": chat_id,
                "private_only": True,
                "sender_id": sender_id,
                "sender_type": sender_type
            })
            return wrapper

        return decorator

    def on_message_group(
        self,
        chat_id: Optional[Union[str, List[str]]] = None,
        commands: Optional[List[str]] = None,
        filters: Optional[Callable[[Message], bool]] = None,
        sender_id: Optional[Union[str, List[str]]] = None,
        sender_type: Optional[str] = None,  
        allow_forwarded: bool = True,
        allow_files: bool = True,
        allow_stickers: bool = True,
        allow_polls: bool = True,
        allow_contacts: bool = True,
        allow_locations: bool = True,
        min_text_length: Optional[int] = None,
        max_text_length: Optional[int] = None,
        contains: Optional[str] = None,
        startswith: Optional[str] = None,
        endswith: Optional[str] = None,
        case_sensitive: bool = False
    ):
        """
        Sync decorator for handling only group messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                
                if not message.is_group:
                    return

                
                if chat_id:
                    if isinstance(chat_id, str) and message.chat_id != chat_id:
                        return
                    if isinstance(chat_id, list) and message.chat_id not in chat_id:
                        return

                
                if sender_id:
                    if isinstance(sender_id, str) and message.sender_id != sender_id:
                        return
                    if isinstance(sender_id, list) and message.sender_id not in sender_id:
                        return

                
                if sender_type and message.sender_type != sender_type:
                    return

                
                if not allow_forwarded and message.forwarded_from:
                    return

                
                if not allow_files and message.file:
                    return
                if not allow_stickers and message.sticker:
                    return
                if not allow_polls and message.poll:
                    return
                if not allow_contacts and message.contact_message:
                    return
                if not allow_locations and (message.location or message.live_location):
                    return

                
                if message.text:
                    text = message.text if case_sensitive else message.text.lower()
                    if min_text_length and len(message.text) < min_text_length:
                        return
                    if max_text_length and len(message.text) > max_text_length:
                        return
                    if contains and (contains if case_sensitive else contains.lower()) not in text:
                        return
                    if startswith and not text.startswith(startswith if case_sensitive else startswith.lower()):
                        return
                    if endswith and not text.endswith(endswith if case_sensitive else endswith.lower()):
                        return

                
                if commands:
                    if not message.text:
                        return
                    parts = message.text.strip().split()
                    cmd = parts[0].lstrip("/")
                    if cmd not in commands:
                        return
                    message.args = parts[1:]

                
                if filters and not filters(message):
                    return

                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "commands": commands,
                "chat_id": chat_id,
                "group_only": True,
                "sender_id": sender_id,
                "sender_type": sender_type
            })
            return wrapper

        return decorator

    def on_message(
        self, 
        filters: Optional[Callable[[Message], bool]] = None, 
        commands: Optional[List[str]] = None
    ):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if filters and not filters(message):
                    return
                if commands:
                    if not getattr(message, "is_command", False):
                        return
                    cmd = message.text.split()[0].lstrip("/") if message.text else ""
                    if cmd not in commands:
                        return
                return func(bot, message)
            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_file(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.file:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "file_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_forwarded(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_forwarded:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "forwarded_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_reply(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_reply:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "reply_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_text(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.text:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "text_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_media(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_media:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "media_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_sticker(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.sticker:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "sticker_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_contact(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_contact:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "contact_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_location(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_location:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "location_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def on_message_poll(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            def wrapper(bot, message: Message):
                if not message.is_poll:
                    return
                if filters and not filters(message):
                    return
                return func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "poll_only": True,
                "commands":commands
            })
            return wrapper
        return decorator

    def message_handler(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            self._message_handlers.append({
                "func": func,
                "filters": filters,
                "commands": commands
            })
            return func
        return decorator
    def on_update(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            self._message_handlers.append({
                "func": func,
                "filters": filters,
                "commands": commands
            })
            return func
        return decorator

    def on_callback(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, Message], None]):
            if not hasattr(self, "_callback_handlers"):
                self._callback_handlers = []
            self._callback_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator 
    def callback_query(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, Message], None]):
            if not hasattr(self, "_callback_handlers"):
                self._callback_handlers = []
            self._callback_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator
    def callback_query_handler(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, Message], None]):
            if not hasattr(self, "_callback_handlers"):
                self._callback_handlers = []
            self._callback_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator
    def _handle_inline_query(self, inline_message: InlineMessage):
        aux_button_id = inline_message.aux_data.button_id if inline_message.aux_data else None

        for handler in self._inline_query_handlers:
            if handler["button_id"] is None or handler["button_id"] == aux_button_id:
                try:
                    handler["func"](self, inline_message)
                except Exception as e:
                    print(f"Error in inline query handler: {e}")

    def on_inline_query(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, InlineMessage], None]):
            self._inline_query_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator

    
    def _process_update(self, update: dict):
        import threading

        if update.get("type") == "ReceiveQuery":
            msg = update.get("inline_message", {})
            context = InlineMessage(bot=self, raw_data=msg)

            
            if hasattr(self, "_callback_handlers"):
                for handler in self._callback_handlers:
                    cb_id = getattr(context.aux_data, "button_id", None)
                    if not handler["button_id"] or handler["button_id"] == cb_id:
                        threading.Thread(target=handler["func"], args=(self, context), daemon=True).start()

            
            threading.Thread(target=self._handle_inline_query, args=(context,), daemon=True).start()
            return

        if update.get("type") == "NewMessage":
            msg = update.get("new_message", {})
            try:
                if msg.get("time") and (time.time() - float(msg["time"])) > 20:
                    return
            except Exception:
                return

            context = Message(bot=self, 
                              chat_id=update.get("chat_id"), 
                              message_id=msg.get("message_id"), 
                              sender_id=msg.get("sender_id"), 
                              text=msg.get("text"), 
                              raw_data=msg)

            if context.aux_data and self._callback_handlers:
                for handler in self._callback_handlers:
                    if not handler["button_id"] or context.aux_data.button_id == handler["button_id"]:
                        threading.Thread(target=handler["func"], args=(self, context), daemon=True).start()
                        return

            if self._message_handlers:
                for handler in self._message_handlers:
                    if handler["commands"]:
                        if not context.text or not context.text.startswith("/"):
                            continue
                        parts = context.text.split()
                        cmd = parts[0][1:]
                        if cmd not in handler["commands"]:
                            continue
                        context.args = parts[1:]

                    if handler["filters"] and not handler["filters"](context):
                        continue

                    threading.Thread(target=handler["func"], args=(self, context), daemon=True).start()
                    continue

    def get_updates(
            self,
            offset_id: Optional[str] = None,
            limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get updates from the Rubika Bot API.

        Parameters:
            offset_id (str, optional): The ID of the update to start receiving updates from. Defaults to None.
            limit (int, optional): The maximum number of updates to retrieve. Defaults to None.

        Returns:
            dict: The response containing the updates.
        """
        data = {}
        if offset_id:
            data["offset_id"] = offset_id
        if limit:
            data["limit"] = limit

        # Use the POST method to send the request and return the response
        return self._post("getUpdates", data)
    def update_webhook(
        self,
        offset_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        data = {}
        if offset_id:
            data["offset_id"] = offset_id
        if limit:
            data["limit"] = limit
        return list(requests.get(self.web_hook).json())
    def _is_duplicate(self, message_id: str, max_age_sec: int = 300) -> bool:
        now = time.time()

        expired = [mid for mid, ts in self._processed_message_ids.items() if now - ts > max_age_sec]
        for mid in expired:
            del self._processed_message_ids[mid]

        if message_id in self._processed_message_ids:
            return True

        self._processed_message_ids[message_id] = now
        return False

    def run(
        self,
        debug=False,
        sleep_time=0.1,
        webhook_timeout=20,
        update_limit=100,
        retry_delay=5,
        stop_on_error=False,
        max_errors=None,
        max_runtime=None,
        allowed_update_types=None,
        ignore_duplicate_messages=True,
        skip_inline_queries=False,
        skip_channel_posts=False,
        skip_service_messages=False,
        skip_edited_messages=False,
        skip_bot_messages=False,
        log_file=None,
        print_exceptions=True,
        error_handler=None,
        shutdown_hook=None,
        log_to_console=True,
        custom_update_fetcher=None,
        custom_update_processor=None,
        message_filter=None,
        notify_on_error=False,
        notification_handler=None,
    ):
        import time
        from typing import Dict
        if debug:
            print("[DEBUG] Bot started running server...")

        self._processed_message_ids: Dict[str, float] = {}
        error_count = 0
        start_time = time.time()

        try:
            while True:
                try:
                    
                    if max_runtime and (time.time() - start_time > max_runtime):
                        if debug:
                            print("[DEBUG] Max runtime reached, stopping...")
                        break

                    
                    if self.web_hook:
                        updates = custom_update_fetcher() if custom_update_fetcher else self.update_webhook()
                        if isinstance(updates, list):
                            for item in updates:
                                data = item.get("data", {})
                                received_at_str = item.get("received_at")

                                if received_at_str:
                                    try:
                                        received_at_ts = datetime.datetime.strptime(received_at_str, "%Y-%m-%d %H:%M:%S").timestamp()
                                        if time.time() - received_at_ts > webhook_timeout:
                                            continue
                                    except (ValueError, TypeError):
                                        pass

                                update = data.get("update") or (
                                    {"type": "ReceiveQuery", "inline_message": data.get("inline_message")}
                                    if "inline_message" in data else None
                                )
                                if not update:
                                    continue

                                
                                if skip_inline_queries and update.get("type") == "ReceiveQuery":
                                    continue
                                if skip_channel_posts and update.get("type") == "ChannelPost":
                                    continue
                                if skip_service_messages and update.get("type") == "ServiceMessage":
                                    continue
                                if skip_edited_messages and update.get("type") == "EditedMessage":
                                    continue
                                if skip_bot_messages and update.get("from", {}).get("is_bot"):
                                    continue
                                if allowed_update_types and update.get("type") not in allowed_update_types:
                                    continue

                                message_id = (
                                    update.get("new_message", {}).get("message_id")
                                    if update.get("type") == "NewMessage"
                                    else update.get("inline_message", {}).get("message_id")
                                    if update.get("type") == "ReceiveQuery"
                                    else update.get("message_id")
                                )

                                if message_id is not None:
                                    message_id = str(message_id)

                                if message_id and (not ignore_duplicate_messages or not self._is_duplicate(received_at_str)):
                                    if message_filter and not message_filter(update):
                                        continue
                                    if custom_update_processor:
                                        custom_update_processor(update)
                                    else:
                                        self._process_update(update)
                                    if message_id:
                                        self._processed_message_ids[message_id] = time.time()

                    
                    else:
                        updates = custom_update_fetcher() if custom_update_fetcher else self.get_updates(offset_id=self._offset_id, limit=update_limit)
                        if updates and updates.get("data"):
                            for update in updates["data"].get("updates", []):
                                if allowed_update_types and update.get("type") not in allowed_update_types:
                                    continue

                                message_id = (
                                    update.get("new_message", {}).get("message_id")
                                    if update.get("type") == "NewMessage"
                                    else update.get("inline_message", {}).get("message_id")
                                    if update.get("type") == "ReceiveQuery"
                                    else update.get("message_id")
                                )

                                if message_id is not None:
                                    message_id = str(message_id)

                                if message_id and (not ignore_duplicate_messages or not self._is_duplicate(message_id)):
                                    if message_filter and not message_filter(update):
                                        continue
                                    if custom_update_processor:
                                        custom_update_processor(update)
                                    else:
                                        self._process_update(update)
                                    if message_id:
                                        self._processed_message_ids[message_id] = time.time()

                            self._offset_id = updates["data"].get("next_offset_id", self._offset_id)

                    if sleep_time:
                        time.sleep(sleep_time)

                except Exception as e:
                    error_count += 1
                    if log_to_console:
                        print(f"Error in run loop: {e}")
                    if log_file:
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(f"{datetime.datetime.now()} - ERROR: {e}\n")
                    if print_exceptions:
                        import traceback
                        traceback.print_exc()
                    if error_handler:
                        error_handler(e)
                    if notify_on_error and notification_handler:
                        notification_handler(e)

                    if max_errors and error_count >= max_errors and stop_on_error:
                        break

                    time.sleep(retry_delay)

        finally:
            if shutdown_hook:
                shutdown_hook()
            if debug:
                print("Bot stopped and session closed.")

    def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Optional[Literal["New", "Removed"]] = None,
        delete_after = None,
        parse_mode = None
    ) -> Dict[str, Any]:
        """
        Send a text message to a chat.
        """
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification
        }
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if chat_keypad_type:
            payload["chat_keypad_type"] = chat_keypad_type

        return self._post("sendMessage", payload)

    def _get_client(self):
        if self.session_name:
            return Client_get(self.session_name,self.auth,self.Key,self.platform)
        else :
            return Client_get(show_last_six_words(self.token),self.auth,self.Key,self.platform)
    from typing import Union

    def check_join(self, channel_guid: str, chat_id: str = None) -> Union[bool, list[str]]:
        client = self._get_client()

        if chat_id:
            chat_info = self.get_chat(chat_id).get('data', {}).get('chat', {})
            username = chat_info.get('username')
            user_id = chat_info.get('user_id')

            if username:
                members = self.get_all_member(channel_guid, search_text=username).get('in_chat_members', [])
                return any(m.get('username') == username for m in members)

            elif user_id:
                member_guids = client.get_all_members(channel_guid, just_get_guids=True)
                return user_id in member_guids

            return False

        return False

    def get_url_file(self,file_id):
        data = self._post("getFile", {'file_id': file_id})
        return data.get("data").get("download_url")
    

    def get_all_member(
        self,
        channel_guid: str,
        search_text: str = None,
        start_id: str = None,
        just_get_guids: bool = False
    ):
        client = self._get_client()
        return client.get_all_members(channel_guid, search_text, start_id, just_get_guids)

    def send_poll(
        self,
        chat_id: str,
        question: str,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Send a poll to a chat.
        """
        return self._post("sendPoll", {
            "chat_id": chat_id,
            "question": question,
            "options": options
        })

    def send_location(
            self,
            chat_id: str,
            latitude: float,
            longitude: float,
            disable_notification: bool = False,
            inline_keypad: Optional[Dict[str, Any]] = None,
            reply_to_message_id: Optional[str] = None,
            chat_keypad_type: Optional[Literal["New", "Removed"]] = None
    ) -> Dict[str, Any]:
        """
        Send a location to a chat.

        Parameters:
            chat_id (str): The unique identifier for the target chat.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            disable_notification (bool, optional): If True, the message will be sent without a notification. Defaults to False.
            inline_keypad (dict, optional): Inline keypad options. Defaults to None.
            reply_to_message_id (str, optional): If the message is a reply, this parameter is the ID of the original message. Defaults to None.
            chat_keypad_type (Literal["New", "Removed"], optional): The type of keypad (New or Removed). Defaults to None.

        Returns:
            dict: The response from the API after sending the location.
        """
        payload = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "disable_notification": disable_notification,
            "inline_keypad": inline_keypad,
            "reply_to_message_id": reply_to_message_id,
            "chat_keypad_type": chat_keypad_type
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._post("sendLocation", payload)

    def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Send a contact to a chat.
        """
        return self._post("sendContact", {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number
        })
    def download(self,file_id: str, save_as: str = None, chunk_size: int = 1024 * 512, timeout_sec: int = 60, verbose: bool = False):
        """
        Download a file from server using its file_id with chunked transfer,
        progress bar, file extension detection, custom filename, and timeout.

        If save_as is not provided, filename will be extracted from
        Content-Disposition header or Content-Type header extension.

        Parameters:
            file_id (str): The file ID to fetch the download URL.
            save_as (str, optional): Custom filename to save. If None, automatically detected.
            chunk_size (int, optional): Size of each chunk in bytes. Default 512KB.
            timeout_sec (int, optional): HTTP timeout in seconds. Default 60.
            verbose (bool, optional): Show progress messages. Default True.

        Returns:
            bool: True if success, raises exceptions otherwise.
        """
        try:
            url = self.get_url_file(file_id)
            if not url:
                raise ValueError("Download URL not found in response.")
        except Exception as e:
            raise ValueError(f"Failed to get download URL: {e}")

        try:
            with requests.get(url, stream=True, timeout=timeout_sec) as resp:
                if resp.status_code != 200:
                    raise requests.HTTPError(f"Failed to download file. Status code: {resp.status_code}")

                if not save_as:
                    content_disp = resp.headers.get("Content-Disposition", "")
                    match = re.search(r'filename="?([^\";]+)"?', content_disp)
                    if match:
                        save_as = match.group(1)
                    else:
                        content_type = resp.headers.get("Content-Type", "").split(";")[0]
                        extension = mimetypes.guess_extension(content_type) or ".bin"
                        save_as = f"{file_id}{extension}"

                total_size = int(resp.headers.get("Content-Length", 0))
                progress = tqdm(total=total_size, unit="B", unit_scale=True)

                with open(save_as, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            progress.update(len(chunk))

                progress.close()
                if verbose:
                    print(f"File saved as: {save_as}")

                return True

        except Exception as e:
            raise RuntimeError(f"Download failed: {e}")
    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get chat info."""
        return self._post("getChat", {"chat_id": chat_id})

    def upload_media_file(self, upload_url: str, name: str, path: Union[str, Path]) -> str:
        is_temp_file = False

        if isinstance(path, str) and path.startswith("http"):
            response = requests.get(path)
            if response.status_code != 200:
                raise Exception(f"Failed to download file from URL ({response.status_code})")
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(response.content)
            temp_file.close()
            path = temp_file.name
            is_temp_file = True

        file_size = os.path.getsize(path)

        with open(path, 'rb') as f:
            progress_bar = None

            if self.show_progress:
                progress_bar = tqdm(
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f'Uploading : {name}',
                    bar_format='{l_bar}{bar:100}{r_bar}',
                    colour='cyan'
                )

            class FileWithProgress:
                def __init__(self, file, progress):
                    self.file = file
                    self.progress = progress

                def read(self, size=-1):
                    data = self.file.read(size)
                    if self.progress:
                        self.progress.update(len(data))
                    return data

                def __getattr__(self, attr):
                    return getattr(self.file, attr)

            file_with_progress = FileWithProgress(f, progress_bar)

            files = {
                'file': (name, file_with_progress, 'application/octet-stream')
            }

            response = requests.post(upload_url, files=files)

            if progress_bar:
                progress_bar.close()

        if is_temp_file:
            os.remove(path)

        if response.status_code != 200:
            raise Exception(f"Upload failed ({response.status_code}): {response.text}")

        data = response.json()
        return data.get('data', {}).get('file_id')

    def send_button_join(
    self, 
    chat_id, 
    title_button :  Union[str, list], 
    username :  Union[str, list], 
    text, 
    reply_to_message_id=None, 
    id="None"
):
        from .button import InlineBuilder
        builder = InlineBuilder()

        
        if isinstance(username, (list, tuple)) and isinstance(title_button, (list, tuple)):
            for t, u in zip(title_button, username):
                builder = builder.row(
                    InlineBuilder().button_join_channel(
                        text=t,
                        id=id,
                        username=u
                    )
                )

        
        elif isinstance(username, (list, tuple)) and isinstance(title_button, str):
            for u in username:
                builder = builder.row(
                    InlineBuilder().button_join_channel(
                        text=title_button,
                        id=id,
                        username=u
                    )
                )

        
        else:
            builder = builder.row(
                InlineBuilder().button_join_channel(
                    text=title_button,
                    id=id,
                    username=username
                )
            )

        return self.send_message(
            chat_id=chat_id,
            text=text,
            inline_keypad=builder.build(),
            reply_to_message_id=reply_to_message_id
        )


    def send_button_url(
        self, 
        chat_id, 
        title_button :  Union[str, list], 
        url :  Union[str, list], 
        text, 
        reply_to_message_id=None, 
        id="None"
    ):
        from .button import InlineBuilder
        builder = InlineBuilder()

        
        if isinstance(url, (list, tuple)) and isinstance(title_button, (list, tuple)):
            for t, u in zip(title_button, url):
                builder = builder.row(
                    InlineBuilder().button_url_link(
                        text=t,
                        id=id,
                        url=u
                    )
                )

        
        elif isinstance(url, (list, tuple)) and isinstance(title_button, str):
            for u in url:
                builder = builder.row(
                    InlineBuilder().button_url_link(
                        text=title_button,
                        id=id,
                        url=u
                    )
                )

        
        else:
            builder = builder.row(
                InlineBuilder().button_url_link(
                    text=title_button,
                    id=id,
                    url=url
                )
            )

        return self.send_message(
            chat_id=chat_id,
            text=text,
            inline_keypad=builder.build(),
            reply_to_message_id=reply_to_message_id
        )


    def get_upload_url(self, media_type: Literal['File', 'Image', 'Voice', 'Music', 'Gif','Video']) -> str:
        allowed = ['File', 'Image', 'Voice', 'Music', 'Gif','Video']
        if media_type not in allowed:
            raise ValueError(f"Invalid media type. Must be one of {allowed}")
        result = self._post("requestSendFile", {"type": media_type})
        return result.get("data", {}).get("upload_url")
    def _send_uploaded_file(self, chat_id: str, file_id: str,type_file : str = "file",text: Optional[str] = None, chat_keypad: Optional[Dict[str, Any]] = None, inline_keypad: Optional[Dict[str, Any]] = None, disable_notification: bool = False, reply_to_message_id: Optional[str] = None, chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None") -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "file_id": file_id,
            "text": text,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type,
        }
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)

        resp = self._post("sendFile", payload)
        message_id_put = resp["data"]["message_id"]
        result = {
            "status": resp.get("status"),
            "status_det": resp.get("status_det"),
            "file_id": file_id,
            "text":text,
            "message_id": message_id_put,
            "send_to_chat_id": chat_id,
            "reply_to_message_id": reply_to_message_id,
            "disable_notification": disable_notification,
            "type_file": type_file,
            "raw_response": resp,
            "chat_keypad":chat_keypad,
            "inline_keypad":inline_keypad,
            "chat_keypad_type":chat_keypad_type
        }
        import json
        return json.dumps(result, ensure_ascii=False, indent=4)
    def send_file(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("File")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=caption,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def re_send_file(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        caption: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("File")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=caption,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_document(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("File")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_music(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("Music")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_video(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("Video")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_voice(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("Voice")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_image(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("Image")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    def send_gif(
        self,
        chat_id: str,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad_type: Optional[Literal["New", "Removed", "None"]] = "None"
    ) -> Dict[str, Any]:
        if path:
            file_name = file_name or Path(path).name
            upload_url = self.get_upload_url("Gif")
            file_id = self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return self._send_uploaded_file(
            chat_id=chat_id,
            file_id=file_id,
            text=text,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    

    def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False
    ) -> Dict[str, Any]:
        """Forward a message from one chat to another."""
        return self._post("forwardMessage", {
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "to_chat_id": to_chat_id,
            "disable_notification": disable_notification
        })

    def edit_message_text(
        self,
        chat_id: str,
        message_id: str,
        text: str
    ) -> Dict[str, Any]:
        """Edit text of an existing message."""
        return self._post("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        })

    def edit_inline_keypad(
        self,
        chat_id: str,
        message_id: str,
        inline_keypad: Dict[str, Any],
        text : str = None
    ) -> Dict[str, Any]:
        """Edit inline keypad of a message."""
        if text is not None:self._post("editMessageText", {"chat_id": chat_id,"message_id": message_id,"text": text})
        return self._post("editMessageKeypad", {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_keypad": inline_keypad
        })

    def delete_message(self, chat_id: str, message_id: str) -> Dict[str, Any]:
        """Delete a message from chat."""
        return self._post("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    def set_commands(self, bot_commands: List[Dict[str, str]]) -> Dict[str, Any]:
        """Set bot commands."""
        return self._post("setCommands", {"bot_commands": bot_commands})

    def update_bot_endpoint(self, url: str, type: str) -> Dict[str, Any]:
        """Update bot endpoint (Webhook or Polling)."""
        return self._post("updateBotEndpoints", {
            "url": url,
            "type": type
        })

    def remove_keypad(self, chat_id: str) -> Dict[str, Any]:
        """Remove chat keypad."""
        return self._post("editChatKeypad", {
            "chat_id": chat_id,
            "chat_keypad_type": "Removed"
        })

    def edit_chat_keypad(self, chat_id: str, chat_keypad: Dict[str, Any]) -> Dict[str, Any]:
        """Edit or add new chat keypad."""
        return self._post("editChatKeypad", {
            "chat_id": chat_id,
            "chat_keypad_type": "New",
            "chat_keypad": chat_keypad
        })
    def get_name(self, chat_id: str) -> str:
        try:
            chat = self.get_chat(chat_id)
            chat_info = chat.get("data", {}).get("chat", {})
            first_name = chat_info.get("first_name", "")
            last_name = chat_info.get("last_name", "")
            
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
            else:
                return "Unknown"
        except Exception:
            return "Unknown"
    def get_username(self, chat_id: str) -> str:
        chat_info = self.get_chat(chat_id).get("data", {}).get("chat", {})
        return chat_info.get("username", "None")