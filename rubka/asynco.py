import asyncio,aiohttp,aiofiles,time,datetime,json,tempfile,os,sys,subprocess,mimetypes,time, hashlib,sqlite3
from typing import List, Optional, Dict, Any, Literal, Callable, Union,Set
from collections import OrderedDict
from .exceptions import APIRequestError,raise_for_status,InvalidAccessError,InvalidInputError,TooRequestError,InvalidTokenError
from .adaptorrubka import Client as Client_get
from .logger import logger
from .rubino import Bot as Rubino
from . import filters
try:from .context import Message, InlineMessage
except (ImportError, ModuleNotFoundError):from context import Message, InlineMessage
try:from .button import ChatKeypadBuilder, InlineBuilder
except (ImportError, ModuleNotFoundError):from button import ChatKeypadBuilder, InlineBuilder
class FeatureNotAvailableError(Exception):
    pass

from tqdm.asyncio import tqdm
from urllib.parse import urlparse, parse_qs

from pathlib import Path
from tqdm import tqdm
API_URL = "https://botapi.rubika.ir/v3"

def install_package(package_name: str) -> bool:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

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

def get_installed_version(package_name: str) -> Optional[str]:
    if version is None:
        return "unknown"
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None

async def get_latest_version(package_name: str) -> Optional[str]:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get("info", {}).get("version")
    except Exception:
        return None

async def check_rubka_version():
    package_name = "rubka"
    installed_version = get_installed_version(package_name)
    if installed_version is None:
        return
    
    latest_version = await get_latest_version(package_name)
    if latest_version is None:
        return
    
    if installed_version != latest_version:
        print(f"CRITICAL WARNING: Your installed version of '{package_name}' is outdated.")
        print("This poses a serious risk to stability, security, and compatibility with current features.")
        print(f"- Installed version : {installed_version}")
        print(f"- Latest version    : {latest_version}")
        print("\nImmediate action is required.")
        print(f"Run the following command to update safely:")
        print(f"\n    pip install {package_name}=={latest_version}\n")
        print("Delaying this update may result in unexpected crashes, data loss, or broken functionality.")
        print("Stay up-to-date to ensure full support and access to the latest improvements.")
        print("For new methods and updates, visit: @rubka_library\n")



def show_last_six_words(text: str) -> str:
    text = text.strip()
    return text[-6:]
class AttrDict(dict):
    def __getattr__(self, item):
        value = self.get(item)
        if isinstance(value, dict):
            return AttrDict(value)
        return value

class Robot:
    """
Main asynchronous class to interact with the Rubika Bot API.

This class handles sending and receiving messages, inline queries, callbacks,
and manages sessions and API interactions. It is initialized with a bot token
and provides multiple optional parameters for configuration.

Attributes:
    token (str): Bot token used for authentication with Rubika Bot API.
    session_name (str | None): Optional session name for storing session data.
    auth (str | None): Optional authentication string for advanced features related to account key.
    Key (str | None): Optional account key for additional authorization if required.
    platform (str): Platform type, default is 'web'.
    web_hook (str | None): Optional webhook URL for receiving updates.
    timeout (int): Timeout for API requests in seconds (default 10).
    show_progress (bool): Whether to show progress for long operations (default False).
    raise_errors (bool): Whether to raise exceptions on API errors (default True).
    proxy (str | None): Optional proxy URL to route requests through.
    retries (int): Number of times to retry a failed API request (default 2).
    retry_delay (float): Delay between retries in seconds (default 0.5).
    user_agent (str | None): Custom User-Agent header for requests.
    safeSendMode (bool): If True, messages are sent safely. If reply fails using message_id, sends without message_id (default False).
    max_cache_size (int): Maximum number of processed messages stored to prevent duplicates (default 1000).
    max_msg_age (int): Maximum age of messages in seconds to consider for processing (default 20).

Example:
```python
import asyncio
from rubka.asynco import Robot, filters, Message

bot = Robot(token="YOUR_BOT_TOKEN", safeSendMode=False, max_cache_size=1000)

@bot.on_message(filters.is_command.start)
async def start_command(bot: Robot, message: Message):
    await message.reply("Hello!")

asyncio.run(bot.run())
```
Notes:

token is mandatory, all other parameters are optional.

safeSendMode ensures reliable message sending even if replying by message_id fails.

max_cache_size and max_msg_age help manage duplicate message processing efficiently.
"""

    def __init__(self, token: str, session_name: str = None, auth: str = None, Key: str = None, platform: str = "web", web_hook: str = None, timeout: int = 10, show_progress: bool = False, raise_errors: bool = True,proxy: str = None,retries: int = 2,retry_delay: float = 0.5,user_agent: str = None,safeSendMode = False,max_cache_size: int = 2000,max_msg_age : int = 60,chunk_size : int = 64 * 1024):
        self.token = token
        self._inline_query_handlers: List[dict] = []
        self.timeout = timeout
        self.auth = auth
        self.chunk_size = chunk_size
        self.safeSendMode = safeSendMode 
        self.user_agent = user_agent
        self.proxy = proxy
        self.max_msg_age = max_msg_age
        self.retries = retries
        self.retry_delay = retry_delay
        self.raise_errors = raise_errors
        self.show_progress = show_progress
        self.session_name = session_name
        self.Key = Key
        self.platform = platform
        self.web_hook = web_hook
        self._offset_id: Optional[str] = None
        self._aiohttp_session: aiohttp.ClientSession = None
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self._callback_handler = None
        self._processed_message_ids = OrderedDict()
        self._max_cache_size = max_cache_size        
        self._callback_handlers: List[dict] = []
        self._edited_message_handlers = []
        self._message_saver_enabled = False
        self._max_messages = None
        self._db_path = os.path.join(os.getcwd(), "RubkaSaveMessage.db")
        self._ensure_db()
        self._message_handlers: List[dict] = []

        logger.info(f"Initialized RubikaBot with token: {token[:8]}***")
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._aiohttp_session is None or self._aiohttp_session.closed:
            connector = aiohttp.TCPConnector(limit=100, ssl=False)
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._aiohttp_session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self._aiohttp_session
    async def close(self):
        if self._aiohttp_session and not self._aiohttp_session.closed:
            await self._aiohttp_session.close()
            logger.debug("aiohttp session closed successfully.")
        
    async def _initialize_webhook(self):
        """Initializes and sets the webhook endpoint if provided."""
        if not self.web_hook:
            return
        
        session = await self._get_session()
        try:
            async with session.get(self.web_hook, timeout=self.timeout) as response:
                response.raise_for_status()
                data = await response.json()
                if data:print(f"[INFO] Retrieving WebHook URL information...")
                json_url = data.get('url', self.web_hook)
            for endpoint_type in [
                    "ReceiveUpdate",
                    "ReceiveInlineMessage",
                    "ReceiveQuery",
                    "GetSelectionItem",
                    "SearchSelectionItems"
                ]:
                result = await self.update_bot_endpoint(self.web_hook, endpoint_type)
                if result['status'] =="OK":print(f"✔ Set endpoint type to '{endpoint_type}' — Operation succeeded with status: {result['status']}")
                else:print(f"[ERROR] Failed to set endpoint type '{endpoint_type}': Status code {result['status']}")
            self.web_hook = json_url
        except Exception as e:
            logger.error(f"Failed to set webhook from {self.web_hook}: {e}")
            self.web_hook = None
    async def _post(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_URL}/{self.token}/{method}"
        session = await self._get_session()
        for attempt in range(1, self.retries + 1):
            try:
                headers = {}
                if self.user_agent:headers["User-Agent"] = self.user_agent
                async with session.post(url, json=data, proxy=self.proxy,headers=headers) as response:
                    if response.status in (429, 500, 502, 503, 504):
                        logger.warning(f"[{method}] Got status {response.status}, retry {attempt}/{self.retries}...")
                        if attempt < self.retries:
                            await asyncio.sleep(self.retry_delay)
                            continue
                        response.raise_for_status()

                    response.raise_for_status()
                    try:
                        json_resp = await response.json(content_type=None)
                    except Exception:
                        text_resp = await response.text()
                        logger.error(f"[{method}] Invalid JSON response: {text_resp}")
                        raise APIRequestError(f"Invalid JSON response: {text_resp}")

                    status = json_resp.get("status")
                    if status in {"INVALID_ACCESS", "INVALID_INPUT", "TOO_REQUESTS"}:
                        if self.raise_errors:
                            raise_for_status(json_resp)
                        return AttrDict(json_resp)
                    return AttrDict({**json_resp, **data,"message_id":json_resp.get("data").get("message_id")})

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.warning(f"[{method}] Attempt {attempt}/{self.retries} failed: {e}")
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay)
                    continue
                logger.error(f"[{method}] API request failed after {self.retries} retries: {e}")
                raise APIRequestError(f"API request failed: {e}") from e
    def _make_dup_key(self, message_id: str, update_type: str, msg_data: dict) -> str:
        raw = f"{message_id}:{update_type}:{msg_data.get('text','')}:{msg_data.get('author_guid','')}"
        return hashlib.sha1(raw.encode()).hexdigest()
    async def get_me(self) -> Dict[str, Any]:
        return await self._post("getMe", {})
    async def geteToken(self):
        if (await self.get_me())['status'] != "OK":
            raise InvalidTokenError("The provided bot token is invalid or expired.")
    from typing import Callable, Any, Optional, List


#save message database __________________________

    def _ensure_db(self):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            message_id TEXT NOT NULL,
            sender_id TEXT,
            text TEXT,
            raw_data TEXT,
            time TEXT,
            saved_at INTEGER
        );
        """)
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_chat_message ON messages(chat_id, message_id);")
        conn.commit()
        conn.close()

    def _insert_message(self, record: dict):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO messages
        (chat_id, message_id, sender_id, text, raw_data, time, saved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get("chat_id"),
            record.get("message_id"),
            record.get("sender_id"),
            record.get("text"),
            json.dumps(record.get("raw_data") or {}, ensure_ascii=False),
            record.get("time"),
            int(time.time())
        ))
        conn.commit()
        if getattr(self, "_max_messages", None) is not None:
            cur.execute("SELECT COUNT(*) FROM messages")
            total = cur.fetchone()[0]
            if total > self._max_messages:
                remove_count = total - self._max_messages
                cur.execute(
                    "DELETE FROM messages WHERE id IN (SELECT id FROM messages ORDER BY saved_at ASC LIMIT ?)",
                    (remove_count,)
                )
                conn.commit()

        conn.close()

    def _fetch_message(self, chat_id: str, message_id: str):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT chat_id, message_id, sender_id, text, raw_data, time, saved_at FROM messages WHERE chat_id=? AND message_id=?",
            (chat_id, message_id)
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        chat_id, message_id, sender_id, text, raw_data_json, time_val, saved_at = row
        try:
            raw = json.loads(raw_data_json)
        except:
            raw = {}
        return {
            "chat_id": chat_id,
            "message_id": message_id,
            "sender_id": sender_id,
            "text": text,
            "raw_data": raw,
            "time": time_val,
            "saved_at": saved_at
        }
    async def save_message(self, message: Message):
        try:
            record = {
                "chat_id": getattr(message, "chat_id", None),
                "message_id": getattr(message, "message_id", None),
                "sender_id": getattr(message, "author_guid", None),
                "text": getattr(message, "text", None),
                "raw_data": getattr(message, "raw_data", {}),
                "time": getattr(message, "time", None),
            }
            await asyncio.to_thread(self._insert_message, record)
        except Exception as e:
            print(f"[DB] Error saving message: {e}")

    async def get_message(self, chat_id: str, message_id: str):
        return await asyncio.to_thread(self._fetch_message, chat_id, message_id)

    def start_save_message(self, max_messages: int = 1000):
        if self._message_saver_enabled:
            return
        self._message_saver_enabled = True
        self._max_messages = max_messages
        decorators = [
            "on_message", "on_edited_message", "on_message_file", "on_message_forwarded",
            "on_message_reply", "on_message_text", "on_update", "on_callback",
            "on_callback_query", "callback_query_handler", "callback_query",
            "on_inline_query", "on_inline_query_prefix", "on_message_private", "on_message_group"
        ]

        for decorator_name in decorators:
            if hasattr(self, decorator_name):
                original_decorator = getattr(self, decorator_name)

                def make_wrapper(orig_decorator):
                    def wrapper(*args, **kwargs):
                        decorator = orig_decorator(*args, **kwargs)
                        def inner_wrapper(func):
                            async def inner(bot, message, *a, **kw):
                                try:
                                    await bot.save_message(message)
                                    if getattr(self, "_max_messages", None) is not None:
                                        await asyncio.to_thread(self._prune_old_messages)
                                except Exception as e:
                                    print(f"[DB] Save error: {e}")
                                return await func(bot, message, *a, **kw)
                            return decorator(inner)
                        return inner_wrapper
                    return wrapper

                setattr(self, decorator_name, make_wrapper(original_decorator))
    def _prune_old_messages(self):
        if not hasattr(self, "_max_messages") or self._max_messages is None:
            return
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM messages")
        total = cur.fetchone()[0]
        if total > self._max_messages:
            remove_count = total - self._max_messages
            cur.execute(
                "DELETE FROM messages WHERE id IN (SELECT id FROM messages ORDER BY saved_at ASC LIMIT ?)",
                (remove_count,)
            )
            conn.commit()
        conn.close()

#save message database __________________________ end

#decorator#

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
        Advanced decorator for handling only private messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                
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
                return await func(bot, message)
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
        Advanced decorator for handling only channel messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                
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
                return await func(bot, message)
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
        Advanced decorator for handling only group messages with extended filters.
        """

        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                
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
                return await func(bot, message)
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
    def remove_handler(self, func: Callable):
        """
        Remove a message handler by its original function reference.
        """
        self._message_handlers = [
            h for h in self._message_handlers if h["func"].__wrapped__ != func
        ]
    def on_edited_message(
    self,
    filters: Optional[Callable[[Message], bool]] = None,
    commands: Optional[List[str]] = None
):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if filters and not filters(message):
                    return
                if commands:
                    if not message.is_command:
                        return
                    cmd = message.text.split()[0].lstrip("/")
                    if cmd not in commands:
                        return
                return await func(bot, message)

            self._edited_message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message(
    self,
    filters: Optional[Callable[[Message], bool]] = None,
    commands: Optional[List[str]] = None):
            def decorator(func: Callable[[Any, Message], None]):
                async def wrapper(bot, message: Message):
                    if filters and not filters(message):
                        return
                    if commands:
                        if not message.is_command:
                            return
                        cmd = message.text.split()[0].lstrip("/")
                        if cmd not in commands:
                            return

                    return await func(bot, message)
                self._message_handlers.append({
                    "func": wrapper,
                    "filters": filters,
                    "commands": commands
                })
                self._edited_message_handlers.append({
                    "func": wrapper,
                    "filters": filters,
                    "commands": commands
                })

                return wrapper
            return decorator

    
    def on_message_file(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.file:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "file_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_forwarded(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_forwarded:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "forwarded_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_reply(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_reply:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "reply_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_text(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.text:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "text_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_media(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_media:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "media_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_sticker(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.sticker:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "sticker_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_contact(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_contact:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "contact_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_location(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_location:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "location_only": True,
                "commands": commands
            })
            return wrapper
        return decorator
    def on_message_poll(self, filters: Optional[Callable[[Message], bool]] = None, commands: Optional[List[str]] = None):
        def decorator(func: Callable[[Any, Message], None]):
            async def wrapper(bot, message: Message):
                if not message.is_poll:return
                if filters and not filters(message):return
                return await func(bot, message)

            self._message_handlers.append({
                "func": wrapper,
                "filters": filters,
                "poll_only": True,
                "commands": commands
            })
            return wrapper
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
        def decorator(func: Callable[[Any, Union[Message, InlineMessage]], None]):
            if not hasattr(self, "_callback_handlers"):
                self._callback_handlers = []
            self._callback_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator
    def on_callback_query(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, Union[Message, InlineMessage]], None]):
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

    async def _handle_inline_query(self, inline_message: InlineMessage):
        aux_button_id = inline_message.aux_data.button_id if inline_message.aux_data else None
        for handler in self._inline_query_handlers:
            if handler["button_id"] is None or handler["button_id"] == aux_button_id:
                try:
                    await handler["func"](self, inline_message)
                except Exception as e:
                    raise Exception(f"Error in inline query handler: {e}")

    def on_inline_query(self, button_id: Optional[str] = None):
        def decorator(func: Callable[[Any, InlineMessage], None]):
            self._inline_query_handlers.append({
                "func": func,
                "button_id": button_id
            })
            return func
        return decorator
    def on_inline_query_prefix(self, prefix: str, button_id: Optional[str] = None):
        if not prefix.startswith('/'):
            prefix = '/' + prefix
        def decorator(func: Callable[[Any, InlineMessage], None]):
            async def handler_wrapper(bot_instance, inline_message: InlineMessage):
                if not inline_message.raw_data or 'text' not in inline_message.raw_data:
                    return
                query_text = inline_message.raw_data['text']
                if query_text.startswith(prefix):
                    try:
                        await func(bot_instance, inline_message)
                    except Exception as e:
                        raise Exception(f"Error in inline query prefix handler '{prefix}': {e}")
            self._inline_query_handlers.append({
                "func": handler_wrapper,
                "button_id": button_id                           
            })
            return func 
        return decorator
    async def _process_update(self, update: dict):
        if update.get("type") == "ReceiveQuery":
            msg = update.get("inline_message", {})
            context = InlineMessage(bot=self, raw_data=msg)
            if hasattr(self, "_callback_handlers"):
                for handler in self._callback_handlers:
                    if not handler["button_id"] or getattr(context.aux_data, "button_id", None) == handler["button_id"]:
                        asyncio.create_task(handler["func"](self, context))
            asyncio.create_task(self._handle_inline_query(context))
            return

        if update.get("type") == "NewMessage":
            msg = update.get("new_message", {})
            try:
                if msg.get("time") and (time.time() - float(msg["time"])) > 20:return
            except (ValueError, TypeError):return
            context = Message(bot=self, 
                              chat_id=update.get("chat_id"), 
                              message_id=msg.get("message_id"), 
                              sender_id=msg.get("sender_id"), 
                              text=msg.get("text"), 
                              raw_data=msg)
            if context.aux_data and self._callback_handlers:
                for handler in self._callback_handlers:
                    if not handler["button_id"] or context.aux_data.button_id == handler["button_id"]:
                        asyncio.create_task(handler["func"](self, context))
                        return
            if self._message_handlers:
                for handler_info in self._message_handlers:
                    
                    if handler_info["commands"]:
                        if not context.text or not context.text.startswith("/"):
                            continue  
                        parts = context.text.split()
                        cmd = parts[0][1:]
                        if cmd not in handler_info["commands"]:
                            continue  
                        context.args = parts[1:]
                    if handler_info["filters"]:
                        if not handler_info["filters"](context):
                            continue 
                    if not handler_info["commands"] and not handler_info["filters"]:
                        asyncio.create_task(handler_info["func"](self, context))
                        continue 
                    if handler_info["commands"] or handler_info["filters"]:
                        asyncio.create_task(handler_info["func"](self, context))#kir baba kir
                        continue 
        elif update.get("type") == "UpdatedMessage":
            msg = update.get("updated_message", {})
            if not msg:
                return

            context = Message(
                bot=self,
                chat_id=update.get("chat_id"),
                message_id=msg.get("message_id"),
                text=msg.get("text"),
                sender_id=msg.get("sender_id"),
                raw_data=msg
            )
            if self._edited_message_handlers:
                for handler_info in self._edited_message_handlers:
                    if handler_info["commands"]:
                        if not context.text or not context.text.startswith("/"):
                            continue
                        parts = context.text.split()
                        cmd = parts[0][1:]
                        if cmd not in handler_info["commands"]:
                            continue
                        context.args = parts[1:]
                    if handler_info["filters"]:
                        if not handler_info["filters"](context):
                            continue
                    asyncio.create_task(handler_info["func"](self, context))
                    
    async def get_updates(self, offset_id: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        data = {}
        if offset_id: data["offset_id"] = offset_id
        if limit: data["limit"] = limit
        return await self._post("getUpdates", data)

    async def update_webhook(self, offset_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        session = await self._get_session()
        params = {}
        if offset_id: params['offset_id'] = offset_id
        if limit: params['limit'] = limit
        async with session.get(self.web_hook, params=params) as response:
            response.raise_for_status() 
            return await response.json()

    def _is_duplicate(self, key: str, max_age_sec: int = 300) -> bool:
        now = time.time()
        expired = [mid for mid, ts in self._processed_message_ids.items() if now - ts > max_age_sec]
        for mid in expired:
            del self._processed_message_ids[mid]
        if key in self._processed_message_ids:
            return True
        self._processed_message_ids[key] = now
        if len(self._processed_message_ids) > self._max_cache_size:
            self._processed_message_ids.popitem(last=False)
        return False

    async def run(
    self,
    debug: bool = False,
    sleep_time: float = 0.1,
    webhook_timeout: int = 20,
    update_limit: int = 100,
    retry_delay: float = 5.0,
    stop_on_error: bool = False,
    max_errors: int = 0,
    auto_restart: bool = False,
    max_runtime: Optional[float] = None,
    loop_forever: bool = True,
    allowed_update_types: Optional[List[str]] = None,
    ignore_duplicate_messages: bool = True,
    skip_inline_queries: bool = False,
    skip_channel_posts: bool = False,
    skip_service_messages: bool = False,
    skip_edited_messages: bool = False,
    skip_bot_messages: bool = False,
    log_file: Optional[str] = None,
    log_level: str = "info",
    print_exceptions: bool = True,
    error_handler: Optional[Callable[[Exception], Any]] = None,
    shutdown_hook: Optional[Callable[[], Any]] = None,
    save_unprocessed_updates: bool = False,
    log_to_console: bool = True,
    rate_limit: Optional[float] = None,
    max_message_size: Optional[int] = None,
    ignore_users: Optional[Set[str]] = None,
    ignore_groups: Optional[Set[str]] = None,
    require_auth_token: bool = False,
    only_private_chats: bool = False,
    only_groups: bool = False,
    require_admin_rights: bool = False,
    custom_update_fetcher: Optional[Callable[[], Any]] = None,
    custom_update_processor: Optional[Callable[[Any], Any]] = None,
    process_in_background: bool = False,
    max_queue_size: int = 1000,
    thread_workers: int = 3,
    message_filter: Optional[Callable[[Any], bool]] = None,
    pause_on_idle: bool = False,
    max_concurrent_tasks: Optional[int] = None,
    metrics_enabled: bool = False,
    metrics_handler: Optional[Callable[[dict], Any]] = None,
    notify_on_error: bool = False,
    notification_handler: Optional[Callable[[str], Any]] = None,
    watchdog_timeout: Optional[float] = None,
):
        """
    Starts the bot's main execution loop with extensive configuration options.

    This function handles:
    - Update fetching and processing with optional filters for types and sources.
    - Error handling, retry mechanisms, and automatic restart options.
    - Logging to console and/or files with configurable log levels.
    - Message filtering based on users, groups, chat types, admin rights, and more.
    - Custom update fetchers and processors for advanced use cases.
    - Background processing with threading and task concurrency controls.
    - Metrics collection and error notifications.
    - Optional runtime limits, sleep delays, rate limiting, and watchdog monitoring.

    Parameters
    ----------
    debug : bool
        Enable debug mode for detailed logging and runtime checks.
    sleep_time : float
        Delay between update fetch cycles (seconds).
    webhook_timeout : int
        Timeout for webhook requests (seconds).
    update_limit : int
        Maximum updates to fetch per request.
    retry_delay : float
        Delay before retrying after failure (seconds).
    stop_on_error : bool
        Stop bot on unhandled errors.
    max_errors : int
        Maximum consecutive errors before stopping (0 = unlimited).
    auto_restart : bool
        Automatically restart the bot if it stops unexpectedly.
    max_runtime : float | None
        Maximum runtime in seconds before stopping.
    loop_forever : bool
        Keep the bot running continuously.

    allowed_update_types : list[str] | None
        Limit processing to specific update types.
    ignore_duplicate_messages : bool
        Skip identical messages.
    skip_inline_queries : bool
        Ignore inline query updates.
    skip_channel_posts : bool
        Ignore channel post updates.
    skip_service_messages : bool
        Ignore service messages.
    skip_edited_messages : bool
        Ignore edited messages.
    skip_bot_messages : bool
        Ignore messages from other bots.

    log_file : str | None
        File path for logging.
    log_level : str
        Logging level (debug, info, warning, error).
    print_exceptions : bool
        Print exceptions to console.
    error_handler : callable | None
        Custom function to handle errors.
    shutdown_hook : callable | None
        Function to execute on shutdown.
    save_unprocessed_updates : bool
        Save updates that failed processing.
    log_to_console : bool
        Enable/disable console logging.

    rate_limit : float | None
        Minimum delay between processing updates from the same user/group.
    max_message_size : int | None
        Maximum allowed message size.
    ignore_users : set[str] | None
        User IDs to ignore.
    ignore_groups : set[str] | None
        Group IDs to ignore.
    require_auth_token : bool
        Require users to provide authentication token.
    only_private_chats : bool
        Process only private chats.
    only_groups : bool
        Process only group chats.
    require_admin_rights : bool
        Process only if sender is admin.

    custom_update_fetcher : callable | None
        Custom update fetching function.
    custom_update_processor : callable | None
        Custom update processing function.
    process_in_background : bool
        Run processing in background threads.
    max_queue_size : int
        Maximum updates in processing queue.
    thread_workers : int
        Number of background worker threads.
    message_filter : callable | None
        Function to filter messages.
    pause_on_idle : bool
        Pause processing if idle.
    max_concurrent_tasks : int | None
        Maximum concurrent processing tasks.

    metrics_enabled : bool
        Enable metrics collection.
    metrics_handler : callable | None
        Function to handle metrics.
    notify_on_error : bool
        Send notifications on errors.
    notification_handler : callable | None
        Function to send error notifications.
    watchdog_timeout : float | None
        Maximum idle time before triggering watchdog restart.
    """
        import asyncio, time, datetime, traceback
        from collections import deque
        def _log(msg: str, level: str = "info"):
            level_order = {"debug": 10, "info": 20, "warning": 30, "error": 40}
            if level not in level_order:
                level = "info"
            if level_order[level] < level_order.get(log_level, 20):
                return
            line = f"[{level.upper()}] {datetime.datetime.now().isoformat()} - {msg}"
            if log_to_console:
                print(msg)
            if log_file:
                try:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(line + "\n")
                except Exception:
                    pass

        def _get_sender_and_chat(update: dict):
            
            sender = None
            chat = None
            t = update.get("type")
            if t == "NewMessage":
                nm = update.get("new_message", {})
                sender = nm.get("author_object_guid") or nm.get("author_guid") or nm.get("from_id")
                chat = nm.get("object_guid") or nm.get("chat_id")
            elif t == "ReceiveQuery":
                im = update.get("inline_message", {})
                sender = im.get("author_object_guid") or im.get("author_guid")
                chat = im.get("object_guid") or im.get("chat_id")
            elif t == "UpdatedMessage":
                im = update.get("updated_message", {})
                sender = im.get("author_object_guid") or im.get("author_guid")
                chat = im.get("object_guid") or im.get("chat_id")
            else:
                sender = update.get("author_guid") or update.get("from_id")
                chat = update.get("object_guid") or update.get("chat_id")
            return str(sender) if sender is not None else None, str(chat) if chat is not None else None

        def _is_group_chat(chat_guid: Optional[str]) -> Optional[bool]:
            
            if chat_guid is None:
                return None
            if hasattr(self, "_is_group_chat") and callable(getattr(self, "_is_group_chat")):
                try:
                    return bool(self._is_group_chat(chat_guid))
                except Exception:
                    return None
            return None  

        async def _maybe_notify(err: Exception, context: dict):
            if notify_on_error and notification_handler:
                try:
                    if asyncio.iscoroutinefunction(notification_handler):
                        await notification_handler(err, context)
                    else:
                        
                        notification_handler(err, context)
                except Exception:
                    pass

        async def _handle_error(err: Exception, context: dict):
            if print_exceptions:
                _log("Exception occurred:\n" + "".join(traceback.format_exception(type(err), err, err.__traceback__)), "error")
            else:
                _log(f"Exception occurred: {err}", "error")
            await _maybe_notify(err, context)
            if error_handler:
                try:
                    if asyncio.iscoroutinefunction(error_handler):
                        await error_handler(err, context)
                    else:
                        error_handler(err, context)
                except Exception as e2:
                    _log(f"Error in error_handler: {e2}", "error")

        
        rate_window = deque()
        def _rate_ok():
            if rate_limit is None or rate_limit <= 0:
                return True
            now = time.time()
            
            while rate_window and now - rate_window[0] > 1.0:
                rate_window.popleft()
            if len(rate_window) < int(rate_limit):
                rate_window.append(now)
                return True
            return False

        
        queue = asyncio.Queue(maxsize=max_queue_size) if process_in_background else None
        active_workers = []

        sem = asyncio.Semaphore(max_concurrent_tasks) if max_concurrent_tasks and max_concurrent_tasks > 0 else None

        async def _process(update: dict):
            
            if allowed_update_types and update.get("type") not in allowed_update_types:
                return False

            
            t = update.get("type")
            if skip_inline_queries and t == "ReceiveQuery":
                return False
            if skip_service_messages and t == "ServiceMessage":
                return False
            if skip_channel_posts and t == "ChannelPost":
                return False

            
            sender, chat = _get_sender_and_chat(update)
            if ignore_users and sender and sender in ignore_users:
                return False
            if ignore_groups and chat and chat in ignore_groups:
                return False
            if require_auth_token and not getattr(self, "_has_auth_token", False):
                return False
            if only_private_chats:
                is_group = _is_group_chat(chat)
                if is_group is True:
                    return False
            if only_groups:
                is_group = _is_group_chat(chat)
                if is_group is False:
                    return False
            if skip_bot_messages and getattr(self, "_is_bot_guid", None) and sender == self._is_bot_guid:
                return False

            if max_message_size is not None and max_message_size > 0:
                
                content = None
                if t == "NewMessage":
                    content = (update.get("new_message") or {}).get("text")
                elif t == "ReceiveQuery":
                    content = (update.get("inline_message") or {}).get("text")
                elif t == "UpdatedMessage":
                    content = (update.get("updated_message") or {}).get("text")
                elif "text" in update:
                    content = update.get("text")
                if content and isinstance(content, str) and len(content) > max_message_size:
                    return False

            if message_filter:
                try:
                    if not message_filter(update):
                        return False
                except Exception:
                    
                    pass

            
            if not _rate_ok():
                return False

            
            if custom_update_processor:
                if asyncio.iscoroutinefunction(custom_update_processor):
                    await custom_update_processor(update)
                else:
                    
                    await asyncio.get_running_loop().run_in_executor(None, custom_update_processor, update)
            else:
                
                await self._process_update(update)
            return True

        async def _worker():
            while True:
                update = await queue.get()
                try:
                    if sem:
                        async with sem:
                            await _process(update)
                    else:
                        await _process(update)
                except Exception as e:
                    await _handle_error(e, {"stage": "worker_process", "update": update})
                finally:
                    queue.task_done()

        
        start_ts = time.time()
        error_count = 0
        last_loop_tick = time.time()
        processed_count = 0
        skipped_count = 0
        enqueued_count = 0
        unprocessed_storage = []

        
        if process_in_background:
            n_workers = max(1, int(thread_workers))
            for _ in range(n_workers):
                active_workers.append(asyncio.create_task(_worker()))

        
        await check_rubka_version()
        await self._initialize_webhook()
        await self.geteToken()
        _log("Bot is up and running...", "info")

        try:
            while True:
                try:
                    
                    if max_runtime is not None and (time.time() - start_ts) >= max_runtime:
                        _log("Max runtime reached. Stopping loop.", "warning")
                        break

                    
                    now = time.time()
                    if watchdog_timeout and (now - last_loop_tick) > watchdog_timeout:
                        _log(f"Watchdog triggered (> {watchdog_timeout}s)", "warning")
                        if auto_restart:
                            break
                    last_loop_tick = now

                    
                    received_updates = None
                    if custom_update_fetcher:
                        received_updates = await custom_update_fetcher()
                    elif self.web_hook:
                        webhook_data = await self.update_webhook()
                        received_updates = []
                        if isinstance(webhook_data, list):
                            for item in webhook_data:
                                data = item.get("data", {})

                                received_at_str = item.get("received_at")
                                if received_at_str:
                                    try:
                                        received_at_ts = datetime.datetime.strptime(received_at_str, "%Y-%m-%d %H:%M:%S").timestamp()
                                        if time.time() - received_at_ts > webhook_timeout:
                                            if debug:
                                                _log(f"Skipped old webhook update ({received_at_str})", "debug")
                                            continue
                                    except (ValueError, TypeError):
                                        pass

                                update = None
                                if "update" in data:
                                    update = data["update"]
                                elif "inline_message" in data:
                                    update = {"type": "ReceiveQuery", "inline_message": data["inline_message"]}
                                else:
                                    continue

                                
                                message_id = None
                                if update.get("type") == "NewMessage":
                                    message_id = update.get("new_message", {}).get("message_id")
                                elif update.get("type") == "ReceiveQuery":
                                    message_id = update.get("inline_message", {}).get("message_id")
                                elif update.get("type") == "UpdatedMessage":
                                    message_id = update.get("updated_message", {}).get("message_id")
                                elif "message_id" in update:
                                    message_id = update.get("message_id")

                                
                                dup_ok = True
                                if ignore_duplicate_messages:
                                    key = str(received_at_str) if received_at_str else str(message_id)
                                    dup_ok = (not self._is_duplicate(str(key))) if key else True

                                if message_id and dup_ok:
                                    received_updates.append(update)
                    else:
                        get_updates_response = await self.get_updates(offset_id=self._offset_id, limit=update_limit)
                        received_updates = []
                        if get_updates_response and get_updates_response.get("data"):
                            updates = get_updates_response["data"].get("updates", [])
                            self._offset_id = get_updates_response["data"].get("next_offset_id", self._offset_id)
                            for update in updates:
                                message_id = None
                                if update.get("type") == "NewMessage":
                                    msg_data = update.get("new_message", {})
                                    message_id = msg_data.get("message_id")
                                    text_content = msg_data.get("text", "")
                                    msg_time = int(msg_data.get("time", 0))
                                elif update.get("type") == "ReceiveQuery":
                                    msg_data = update.get("inline_message", {})
                                    message_id = msg_data.get("message_id")
                                    text_content = msg_data.get("text", "")
                                    msg_time = int(msg_data.get("time", 0))
                                elif update.get("type") == "UpdatedMessage":
                                    msg_data = update.get("updated_message", {})
                                    message_id = msg_data.get("message_id")
                                    text_content = msg_data.get("text", "")
                                    msg_time = int(msg_data.get("time", 0))
                                elif "message_id" in update:
                                    message_id = update.get("message_id")
                                else:
                                    msg_time = time.time()
                                    msg_data = update.get("updated_message", {})
                                    message_id = msg_data.get("message_id")
                                    text_content = msg_data.get("text", "")
                                now = int(time.time())
                            
                                if msg_time and (now - msg_time > self.max_msg_age):
                                    continue
                                dup_ok = True
                                if ignore_duplicate_messages and message_id:
                                    dup_key = self._make_dup_key(message_id, update.get("type", ""), msg_data)
                                    dup_ok = not self._is_duplicate(dup_key)
                                if message_id and dup_ok:
                                    received_updates.append(update)
                    if not received_updates:
                        if pause_on_idle and sleep_time == 0:await asyncio.sleep(0.005)
                        else:await asyncio.sleep(sleep_time)
                        if not loop_forever and max_runtime is None:break
                        continue

                    
                    for update in received_updates:
                        if require_admin_rights:
                            
                            sender, _ = _get_sender_and_chat(update)
                            if hasattr(self, "is_admin") and callable(getattr(self, "is_admin")):
                                try:
                                    if not await self.is_admin(sender) if asyncio.iscoroutinefunction(self.is_admin) else not self.is_admin(sender):
                                        skipped_count += 1
                                        continue
                                except Exception:
                                    pass

                        if process_in_background:
                            try:
                                queue.put_nowait(update)
                                enqueued_count += 1
                            except asyncio.QueueFull:
                                
                                skipped_count += 1
                                if save_unprocessed_updates:
                                    unprocessed_storage.append(update)
                        else:
                            try:
                                if sem:
                                    async with sem:
                                        ok = await _process(update)
                                else:
                                    ok = await _process(update)
                                processed_count += 1 if ok else 0
                                skipped_count += 0 if ok else 1
                            except Exception as e:
                                await _handle_error(e, {"stage": "inline_process", "update": update})
                                error_count += 1
                                if save_unprocessed_updates:
                                    unprocessed_storage.append(update)
                                if stop_on_error or (max_errors and error_count >= max_errors):
                                    raise

                    
                    if process_in_background and queue.qsize() > 0:
                        await asyncio.sleep(0)  

                    
                    if debug:
                        _log(f"Loop stats — processed: {processed_count}, enqueued: {enqueued_count}, skipped: {skipped_count}, queue: {queue.qsize() if queue else 0}", "debug")

                    
                    await asyncio.sleep(sleep_time)

                except Exception as e:
                    await _handle_error(e, {"stage": "run_loop"})
                    error_count += 1
                    if stop_on_error or (max_errors and error_count >= max_errors):
                        break
                    await asyncio.sleep(retry_delay)

                
                if not loop_forever and max_runtime is None:
                    break

        finally:
            
            if process_in_background and queue:
                try:
                    await queue.join()
                except Exception:
                    pass
                for w in active_workers:
                    w.cancel()
                
                for w in active_workers:
                    try:
                        await w
                    except Exception:
                        pass

            
            if self._aiohttp_session:
                await self._aiohttp_session.close()

            
            stats = {
                "processed": processed_count,
                "skipped": skipped_count,
                "enqueued": enqueued_count,
                "errors": error_count,
                "uptime_sec": round(time.time() - start_ts, 3),
            }
            if metrics_enabled and metrics_handler:
                try:
                    if asyncio.iscoroutinefunction(metrics_handler):
                        await metrics_handler(stats)
                    else:
                        metrics_handler(stats)
                except Exception:
                    pass

            if shutdown_hook:
                try:
                    if asyncio.iscoroutinefunction(shutdown_hook):
                        await shutdown_hook(stats)
                    else:
                        shutdown_hook(stats)
                except Exception:
                    pass

            print("Bot stopped and session closed.")

        
        if auto_restart:
            
            
            _log("Auto-restart requested. You can call run(...) again as needed.", "warning")
    async def _delete_after_task(self, chat_id: str, message_id: str, delay: int):
        try:
            await asyncio.sleep(delay)
            await self.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            return False
    async def _edit_after_task(self, chat_id: str, message_id: str, text:str, delay: int):
        try:
            await asyncio.sleep(delay)
            await self.edit_message_text(chat_id=chat_id, message_id=message_id,text=text)
        except Exception:
            return False
        
    async def delete_after(self, chat_id: str, message_id: str, delay: int = 30) -> asyncio.Task:
        async def _task():
            await asyncio.sleep(delay)
            try:
                await self.delete_message(chat_id, message_id)
            except Exception:
                pass

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        task = loop.create_task(_task())
        return task

    async def edit_after(self, chat_id: str, message_id: str, text : str, delay: int = 30) -> asyncio.Task:
        async def _task():
            await asyncio.sleep(delay)
            try:
                await self.edit_message_text(chat_id, message_id,text)
            except Exception:
                pass

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        task = loop.create_task(_task())
        return task

    async def send_message(
    self,
    chat_id: str,
    text: str,
    chat_keypad: Optional[Dict[str, Any]] = None,
    inline_keypad: Optional[Dict[str, Any]] = None,
    disable_notification: bool = False,
    reply_to_message_id: Optional[str] = None,
    chat_keypad_type: Optional[Literal["New", "Remove"]] = None,
    delete_after : int = None
) -> Dict[str, Any]:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification,
        }
        if chat_keypad:
            payload["chat_keypad"] = chat_keypad
            payload["chat_keypad_type"] = chat_keypad_type or "New"
        if inline_keypad:
            payload["inline_keypad"] = inline_keypad
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if self.safeSendMode and reply_to_message_id:
            try:
                state = await self._post("sendMessage", payload)
            except Exception:
                payload.pop("reply_to_message_id", None)
                state = await self._post("sendMessage", payload)
        else:
            state = await self._post("sendMessage", payload)
        if delete_after:
            await self.delete_after(chat_id, state.message_id, delete_after)
            return state
        return state
    

    async def send_sticker(
        self,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[Dict[str, Any]] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Optional[Literal['New', 'Remove']] = None,
    ) -> str:
        """
        Send a sticker to a chat.

        Args:
            token: Bot token.
            chat_id: Target chat ID.
            sticker_id: ID of the sticker to send.
            chat_keypad: Optional chat keypad data.
            disable_notification: If True, disables notification.
            inline_keypad: Optional inline keyboard data.
            reply_to_message_id: Optional message ID to reply to.
            chat_keypad_type: Type of chat keypad change ('New' or 'Remove').

        Returns:
            API response as a string.
        """
        data = {
            'chat_id': chat_id,
            'sticker_id': sticker_id,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }
        return await self._post("sendSticker", data)


    async def get_url_file(self,file_id):
        data = await self._post("getFile", {'file_id': file_id})
        return data.get("data").get("download_url")

    def _get_client(self) -> Client_get:
        if self.session_name:
            return Client_get(self.session_name, self.auth, self.Key, self.platform)
        else:
            return Client_get(show_last_six_words(self.token), self.auth, self.Key, self.platform)
    async def send_button_join(
    self, 
    chat_id, 
    title_button : Union[str, list],
    username :  Union[str, list], 
    text,
    reply_to_message_id=None, 
    id="None"):
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
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            inline_keypad=builder.build(),
            reply_to_message_id=reply_to_message_id
        )
    async def send_button_link(
    self, 
    chat_id, 
    title_button: Union[str, list],
    url: Union[str, list], 
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
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            inline_keypad=builder.build(),
            reply_to_message_id=reply_to_message_id
        )

    async def close_poll(self, chat_id: str, message_id: str) -> Dict[str, Any]:
        return await self._post("closePoll", {"chat_id": chat_id, "message_id": message_id})
    async def send_location(self, chat_id: str, latitude: str, longitude: str, disable_notification: bool = False, inline_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, chat_keypad_type: Optional[Literal["New", "Remove"]] = None) -> Dict[str, Any]:
        payload = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude, "disable_notification": disable_notification}
        if inline_keypad: payload["inline_keypad"] = inline_keypad
        if reply_to_message_id: payload["reply_to_message_id"] = reply_to_message_id
        if chat_keypad_type: payload["chat_keypad_type"] = chat_keypad_type
        return await self._post("sendLocation", {k: v for k, v in payload.items() if v is not None})
    async def upload_media_file(self, upload_url: str, name: str, path: Union[str, Path]) -> str:
        session = await self._get_session()
        is_temp_file = False
        if isinstance(path, str) and path.startswith("http"):
            async with session.get(path) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download file from URL ({response.status})")
                content = await response.read()
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(content)
                    path = tmp.name
                    is_temp_file = True

        file_size = os.path.getsize(path)
        chunk_size = self.chunk_size

        progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024,
                            desc=f'Uploading: {name}', colour='cyan', disable=not getattr(self, 'show_progress', True))

        async def file_generator(file_path):
            async with aiofiles.open(file_path, 'rb') as f:
                while chunk := await f.read(chunk_size):
                    progress_bar.update(len(chunk))
                    yield chunk

        form = aiohttp.FormData()
        form.add_field('file', file_generator(path), filename=name, content_type='application/octet-stream')

        try:
            async with session.post(upload_url, data=form, timeout=aiohttp.ClientTimeout(total=None)) as response:
                progress_bar.close()
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"Upload failed ({response.status}): {text}")
                return (await response.json()).get('data', {}).get('file_id')
        except Exception as e:
            raise FeatureNotAvailableError(f"File upload not supported: {e}")
        finally:
            if is_temp_file:
                os.remove(path)
    def get_extension(content_type: str) -> str:
        ext = mimetypes.guess_extension(content_type)
        return ext if ext else ''
    async def download(self, file_id: str, save_as: str = None, chunk_size: int = 1024 * 512,timeout_sec: int = 60, verbose: bool = False):
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
            url = await self.get_url_file(file_id)
            if not url:raise ValueError("Download URL not found in response.")
        except Exception as e:raise ValueError(f"Failed to get download URL: {e}")
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise aiohttp.ClientResponseError(
                            request_info=resp.request_info,
                            history=resp.history,
                            status=resp.status,
                            message="Failed to download file.",
                            headers=resp.headers
                        )
                    if not save_as:
                        content_disp = resp.headers.get("Content-Disposition", "")
                        import re
                        match = re.search(r'filename="?([^\";]+)"?', content_disp)
                        if match:save_as = match.group(1)
                        else:
                            content_type = resp.headers.get("Content-Type", "").split(";")[0]
                            extension = mimetypes.guess_extension(content_type) or ".bin"
                            save_as = f"{file_id}{extension}"
                    total_size = int(resp.headers.get("Content-Length", 0))
                    progress = tqdm(total=total_size, unit="B", unit_scale=True, disable=not verbose)
                    async with aiofiles.open(save_as, "wb") as f:
                        async for chunk in resp.content.iter_chunked(chunk_size):
                            await f.write(chunk)
                            progress.update(len(chunk))

                    progress.close()
                    if verbose:
                        print(f"✅ File saved as: {save_as}")

                    return True

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"HTTP error occurred: {e}")
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("Download timed out.")
        except Exception as e:
            raise Exception(f"Error downloading file: {e}")

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"HTTP error occurred: {e}")
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("The download operation timed out.")
        except Exception as e:
            raise Exception(f"An error occurred while downloading the file: {e}")

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"HTTP error occurred: {e}")
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("The download operation timed out.")
        except Exception as e:
            raise Exception(f"An error occurred while downloading the file: {e}")
    async def get_upload_url(self, media_type: Literal['File', 'Image', 'voice', 'Music', 'Gif', 'Video']) -> str:
        allowed = ['File', 'Image', 'voice', 'Music', 'Gif', 'Video']
        if media_type not in allowed:
            raise ValueError(f"Invalid media type. Must be one of {allowed}")
        result = await self._post("requestSendFile", {"type": media_type})
        return result.get("data", {}).get("upload_url")
    async def _send_uploaded_file(self, chat_id: str, file_id: str,type_file : str = "file",text: Optional[str] = None, chat_keypad: Optional[Dict[str, Any]] = None, inline_keypad: Optional[Dict[str, Any]] = None, disable_notification: bool = False, reply_to_message_id: Optional[str] = None, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        payload = {"chat_id": chat_id, "file_id": file_id, "text": text, "disable_notification": disable_notification, "chat_keypad_type": chat_keypad_type}
        if chat_keypad: payload["chat_keypad"] = chat_keypad
        if inline_keypad: payload["inline_keypad"] = inline_keypad
        if reply_to_message_id: payload["reply_to_message_id"] = str(reply_to_message_id)
        payload["time"] = "10"
        resp = await self._post("sendFile", payload)
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
        return AttrDict(result)
    async def _send_file_generic(self, media_type, chat_id, path, file_id, text, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type):
        if path:
            file_name = file_name or Path(path).name
            upload_url = await self.get_upload_url(media_type)
            file_id = await self.upload_media_file(upload_url, file_name, path)
        if not file_id:
            raise ValueError("Either path or file_id must be provided.")
        return await self._send_uploaded_file(chat_id=chat_id, file_id=file_id, text=text, inline_keypad=inline_keypad, chat_keypad=chat_keypad, reply_to_message_id=reply_to_message_id, disable_notification=disable_notification, chat_keypad_type=chat_keypad_type,type_file=media_type)
    async def send_document(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, text: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("File", chat_id, path, file_id, text, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)
    async def send_file(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, caption: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("File", chat_id, path, file_id, caption, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)
    async def re_send(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, caption: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("File", chat_id, path, file_id, caption, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)  
    async def send_music(
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
    chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None"
    ) -> Dict[str, Any]:
        valid_extensions = {"ogg", "oga", "opus", "flac"}
        extension = "flac"
        if path:
            path_str = str(path)
            if path_str.startswith("http://") or path_str.startswith("https://"):
                parsed = urlparse(path_str)
                base_name = os.path.basename(parsed.path)
            else:
                base_name = os.path.basename(path_str)
            name, ext = os.path.splitext(base_name)

            if file_name is None or not file_name.strip():
                file_name = name or "music"
            ext = ext.lower().replace(".", "")
            if ext in valid_extensions:
                extension = ext
        else:
            if file_name is None:
                file_name = "music"
        return await self._send_file_generic(
            "File",
            chat_id,
            path,
            file_id,
            text,
            f"{file_name}.{extension}",
            inline_keypad,
            chat_keypad,
            reply_to_message_id,
            disable_notification,
            chat_keypad_type
        )
    async def send_gif(
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
    chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None"
    ) -> Dict[str, Any]:
        valid_extensions = {"gif"}
        extension = "gif"
        if path:
            path_str = str(path)
            if path_str.startswith("http://") or path_str.startswith("https://"):
                parsed = urlparse(path_str)
                base_name = os.path.basename(parsed.path)
            else:
                base_name = os.path.basename(path_str)
            name, ext = os.path.splitext(base_name)

            if file_name is None or not file_name.strip():
                file_name = name or "gif"
            ext = ext.lower().replace(".", "")
            if ext in valid_extensions:
                extension = ext
        else:
            if file_name is None:
                file_name = "gif"
        return await self._send_file_generic(
            "File",
            chat_id,
            path,
            file_id,
            text,
            f"{file_name}.{extension}",
            inline_keypad,
            chat_keypad,
            reply_to_message_id,
            disable_notification,
            chat_keypad_type
        )

    async def get_avatar_me(self, save_as: str = None) -> str:
        session = None
        try:
            me_info = await self.get_me()
            avatar = me_info.get('data', {}).get('bot', {}).get('avatar', {})
            file_id = avatar.get('file_id')
            if not file_id:
                return "null"

            file_info = await self.get_url_file(file_id)
            url = file_info.get("download_url") if isinstance(file_info, dict) else file_info

            if save_as:
                session = aiohttp.ClientSession()
                async with session.get(url) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        with open(save_as, "wb") as f:
                            f.write(content)

            return url
        except Exception as e:
            print(f"[get_avatar_me] Error: {e}")
            return "null"
        finally:
            if session and not session.closed:
                await session.close()

    async def get_name(self, chat_id: str) -> str:
        try:
            chat = await self.get_chat(chat_id)
            chat_info = chat.get("data", {}).get("chat", {})
            chat_type = chat_info.get("chat_type", "").lower()
            if chat_type == "user":
                first_name = chat_info.get("first_name", "")
                last_name = chat_info.get("last_name", "")
                full_name = f"{first_name} {last_name}".strip()
                return full_name if full_name else "null"
            elif chat_type in ["group", "channel"]:
                title = chat_info.get("title", "")
                return title if title else "null"
            else:return "null"
        except Exception:return "null"
    async def get_username(self, chat_id: str) -> str:
        chat_info = await self.get_chat(chat_id)
        return chat_info.get("data", {}).get("chat", {}).get("username", "None")
    async def get_chat_admins(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("getChatAdmins", {"chat_id": chat_id})
    async def get_chat_members(self, chat_id: str, start_id: str = "") -> Dict[str, Any]:
        return await self._post("getChatMembers", {"chat_id": chat_id, "start_id": start_id})
    async def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("getChatInfo", {"chat_id": chat_id})
    async def set_chat_title(self, chat_id: str, title: str) -> Dict[str, Any]:
        return await self._post("editChatTitle", {"chat_id": chat_id, "title": title})
    async def set_chat_description(self, chat_id: str, description: str) -> Dict[str, Any]:
        return await self._post("editChatDescription", {"chat_id": chat_id, "description": description})
    async def set_chat_photo(self, chat_id: str, file_id: str) -> Dict[str, Any]:
        return await self._post("editChatPhoto", {"chat_id": chat_id, "file_id": file_id})
    async def remove_chat_photo(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("editChatPhoto", {"chat_id": chat_id, "file_id": "Remove"})
    async def add_member_chat(self, chat_id: str, user_ids: list[str]) -> Dict[str, Any]:
        return await self._post("addChatMembers", {"chat_id": chat_id, "member_ids": user_ids})
    async def ban_member_chat(self, chat_id: str, user_id: str) -> Dict[str, Any]:
        return await self._post("banChatMember", {"chat_id": chat_id, "member_id": user_id})
    async def unban_chat_member(self, chat_id: str, user_id: str) -> Dict[str, Any]:
        return await self._post("unbanChatMember", {"chat_id": chat_id, "member_id": user_id})
    async def restrict_chat_member(self, chat_id: str, user_id: str, until: int = 0) -> Dict[str, Any]:
        return await self._post("restrictChatMember", {"chat_id": chat_id, "member_id": user_id, "until_date": until})
    async def get_chat_member(self, chat_id: str, user_id: str):
        return await self._post("getChatMember", {"chat_id": chat_id, "user_id": user_id})
    async def get_admin_chat(self, chat_id: str):
        return await self._post("getChatAdministrators", {"chat_id": chat_id})
    async def get_chat_member_count(self, chat_id: str):
        return await self._post("getChatMemberCount", {"chat_id": chat_id})
    async def ban_chat_member(self, chat_id: str, user_id: str):
        return await self._post("banChatMember", {"chat_id": chat_id, "user_id": user_id})
    async def promote_chat_member(self, chat_id: str, user_id: str, rights: dict) -> Dict[str, Any]:
        return await self._post("promoteChatMember", {"chat_id": chat_id, "member_id": user_id, "rights": rights})
    async def demote_chat_member(self, chat_id: str, user_id: str) -> Dict[str, Any]:
        return await self._post("promoteChatMember", {"chat_id": chat_id, "member_id": user_id, "rights": {}})
    async def pin_chat_message(self, chat_id: str, message_id: str) -> Dict[str, Any]:
        return await self._post("pinChatMessage", {"chat_id": chat_id, "message_id": message_id})
    async def unpin_chat_message(self, chat_id: str, message_id: str = "") -> Dict[str, Any]:
        return await self._post("unpinChatMessage", {"chat_id": chat_id, "message_id": message_id})
    async def export_chat_invite_link(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("exportChatInviteLink", {"chat_id": chat_id})
    async def revoke_chat_invite_link(self, chat_id: str, link: str) -> Dict[str, Any]:
        return await self._post("revokeChatInviteLink", {"chat_id": chat_id, "invite_link": link})
    async def create_group(self, title: str, user_ids: list[str]) -> Dict[str, Any]:
        return await self._post("createGroup", {"title": title, "user_ids": user_ids})
    async def create_channel(self, title: str, description: str = "") -> Dict[str, Any]:
        return await self._post("createChannel", {"title": title, "description": description})
    async def leave_chat(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("leaveChat", {"chat_id": chat_id})
    async def forward_message(self, from_chat_id: str, message_id: str, to_chat_id: str, disable_notification: bool = False) -> Dict[str, Any]:
        return await self._post("forwardMessage", {"from_chat_id": from_chat_id, "message_id": message_id, "to_chat_id": to_chat_id, "disable_notification": disable_notification})
    async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Dict[str, Any]:
        return await self._post("editMessageText", {"chat_id": chat_id, "message_id": message_id, "text": text})
    async def edit_inline_keypad(self,chat_id: str,message_id: str,inline_keypad: Dict[str, Any],text: str = None) -> Dict[str, Any]:
        if text is not None:await self._post("editMessageText", {"chat_id": chat_id,"message_id": message_id,"text": text})
        return await self._post("editMessageKeypad", {"chat_id": chat_id,"message_id": message_id,"inline_keypad": inline_keypad})
    async def delete_message(self, chat_id: str, message_id: str) -> Dict[str, Any]:
        return await self._post("deleteMessage", {"chat_id": chat_id, "message_id": message_id})
    async def set_commands(self, bot_commands: List[Dict[str, str]]) -> Dict[str, Any]:
        return await self._post("setCommands", {"bot_commands": bot_commands})
    async def update_bot_endpoint(self, url: str, type: str) -> Dict[str, Any]:
        return await self._post("updateBotEndpoints", {"url": url, "type": type})
    async def remove_keypad(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("editChatKeypad", {"chat_id": chat_id, "chat_keypad_type": "Remove"})
    async def edit_chat_keypad(self, chat_id: str, chat_keypad: Dict[str, Any]) -> Dict[str, Any]:
        return await self._post("editChatKeypad", {"chat_id": chat_id, "chat_keypad_type": "New", "chat_keypad": chat_keypad})
    async def send_contact(self, chat_id: str, first_name: str, last_name: str, phone_number: str) -> Dict[str, Any]:
        return await self._post("sendContact", {"chat_id": chat_id, "first_name": first_name, "last_name": last_name, "phone_number": phone_number})
    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        return await self._post("getChat", {"chat_id": chat_id})
    async def send_video(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, text: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("Video", chat_id, path, file_id, text, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)
    async def send_voice(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, text: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("voice", chat_id, path, file_id, text, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)
    async def send_image(self, chat_id: str, path: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, text: Optional[str] = None, file_name: Optional[str] = None, inline_keypad: Optional[Dict[str, Any]] = None, chat_keypad: Optional[Dict[str, Any]] = None, reply_to_message_id: Optional[str] = None, disable_notification: bool = False, chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = "None") -> Dict[str, Any]:
        return await self._send_file_generic("Image", chat_id, path, file_id, text, file_name, inline_keypad, chat_keypad, reply_to_message_id, disable_notification, chat_keypad_type)
    def get_all_member(self, channel_guid: str, search_text: str = None, start_id: str = None, just_get_guids: bool = False):
        client = self._get_client()
        return client.get_all_members(channel_guid, search_text, start_id, just_get_guids)
    async def send_poll(
        self,
        chat_id: str,
        question: str,
        options: List[str],
        type: Literal["Regular", "Quiz"] = "Regular",
        allows_multiple_answers: bool = False,
        is_anonymous: bool = True,
        correct_option_index: Optional[int] = None,
        hint: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        show_results : bool = False,
        inline_keypad : Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[Literal["New", "Remove", "None"]] = None,

    ) -> AttrDict:
        return await self._post(
            "sendPoll", {
                "chat_id": chat_id,
                "question": question,
                "options": options,
                "type": type,
                "allows_multiple_answers": allows_multiple_answers,
                "is_anonymous": is_anonymous,
                "correct_option_index": correct_option_index,
                "explanation": hint,
                "show_results":show_results,
                "reply_to_message_id": reply_to_message_id,
                "disable_notification": disable_notification,
                "chat_keypad": chat_keypad,
                "inline_keypad":inline_keypad,
                "chat_keypad_type": chat_keypad_type,
            }
        )
    async def check_join(self, channel_guid: str, chat_id: str = None) -> Union[bool, list[str]]:
        client = self._get_client()
        if chat_id:
            chat_info_data = await self.get_chat(chat_id)
            chat_info = chat_info_data.get('data', {}).get('chat', {})
            username = chat_info.get('username')
            user_id = chat_info.get('user_id')
            if username:
                result = await asyncio.to_thread(self.get_all_member, channel_guid, search_text=username)
                members = result.get('in_chat_members', [])
                return any(m.get('username') == username for m in members)
            elif user_id:
                member_guids = await asyncio.to_thread(client.get_all_members, channel_guid, just_get_guids=True)
                return user_id in member_guids
        return False