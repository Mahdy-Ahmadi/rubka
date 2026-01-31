from typing import Union
from pathlib import Path
from typing import List, Optional, Dict, Any, Literal, Callable, Union,Set
import re,inspect
import asyncio
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
    "\U00002000-\U000023FF" 
    "]+", 
    flags=re.UNICODE
)

def contains_emoji(text: str) -> bool:
    if not text:return False
    return bool(_EMOJI_PATTERN.search(text))

def count_emojis(text: str) -> int:
    if not text:return 0
    return len(_EMOJI_PATTERN.findall(text))
def contains_link_or_mention(text: str) -> bool:
    if not text:return False
    pattern = re.compile(
        r"(?i)\b("
        r"https?://[^\s]+"
        r"|www\.[^\s]+"
        r"|[a-zA-Z0-9.-]+\.(com|net|org|ir|edu|gov|info|biz|io|me|co|xyz|in|us|uk|ru|tv|cc|app|dev|site|store|cloud|shop)"
        r"|t\.me/[^\s]+"
        r"|telegram\.me/[^\s]+"
        r"|rubika\.(ir|app)/[^\s]+"
        r"|whatsapp\.com/[^\s]+"
        r"|wa\.me/[^\s]+"
        r"|instagram\.com/[^\s]+"
        r"|instagr\.am/[^\s]+"
        r"|youtube\.com/[^\s]+"
        r"|youtu\.be/[^\s]+"
        r"|aparat\.com/[^\s]+"
        r"|discord\.gg/[^\s]+"
        r"|discord\.com/[^\s]+"
        r"|splus\.ir/[^\s]+"
        r"|eitaa\.com/[^\s]+"
        r"|ble\.ir/[^\s]+"
        r"|gap\.im/[^\s]+"
        r"|rubino\.ir/[^\s]+"
        r"|pin\.it/[^\s]+"
        r"|twitter\.com/[^\s]+"
        r"|x\.com/[^\s]+"
        r"|facebook\.com/[^\s]+"
        r"|threads\.net/[^\s]+"
        r"|@\w+"
        r"|\b\d{1,3}(?:\.\d{1,3}){3}\b" 
        r"|\[?[A-F0-9:]{2,39}\]?"
        r")\b"
    )
    return bool(pattern.search(text))
class File:
    def __init__(self, data: dict):
        self.file_id: str = data.get("file_id")
        self.file_name: str = data.get("file_name")
        self.size: str = data.get("size")


class Sticker:
    def __init__(self, data: dict):
        self.sticker_id: str = data.get("sticker_id")
        self.emoji_character: str = data.get("emoji_character")
        self.file = File(data.get("file", {}))





class PollStatus:
    def __init__(self, data: dict):
        self.state: str = data.get("state")
        self.selection_index: int = data.get("selection_index")
        self.percent_vote_options: List[int] = data.get("percent_vote_options", [])
        self.total_vote: int = data.get("total_vote")
        self.show_total_votes: bool = data.get("show_total_votes")


class Poll:
    def __init__(self, data: dict):
        self.question: str = data.get("question")
        self.options: List[str] = data.get("options", [])
        self.poll_status = PollStatus(data.get("poll_status", {}))





class Location:
    def __init__(self, data: dict):
        self.latitude: str = data.get("latitude")
        self.longitude: str = data.get("longitude")


class LiveLocation:
    def __init__(self, data: dict):
        self.start_time: str = data.get("start_time")
        self.live_period: int = data.get("live_period")
        self.current_location = Location(data.get("current_location", {}))
        self.user_id: str = data.get("user_id")
        self.status: str = data.get("status")
        self.last_update_time: str = data.get("last_update_time")


class ContactMessage:
    def __init__(self, data: dict):
        self.phone_number: str = data.get("phone_number")
        self.first_name: str = data.get("first_name")
        self.last_name: str = data.get("last_name")


class ForwardedFrom:
    def __init__(self, data: dict):
        self.type_from: str = data.get("type_from")
        self.message_id: str = data.get("message_id")
        self.from_chat_id: str = data.get("from_chat_id")
        self.from_sender_id: str = data.get("from_sender_id")





class AuxData:
    def __init__(self, data: dict):
        self.start_id: str = data.get("start_id")
        self.button_id: str = data.get("button_id")





class ButtonTextbox:
    def __init__(self, data: dict):
        self.type_line: str = data.get("type_line")
        self.type_keypad: str = data.get("type_keypad")
        self.place_holder: Optional[str] = data.get("place_holder")
        self.title: Optional[str] = data.get("title")
        self.default_value: Optional[str] = data.get("default_value")


class ButtonNumberPicker:
    def __init__(self, data: dict):
        self.min_value: str = data.get("min_value")
        self.max_value: str = data.get("max_value")
        self.default_value: Optional[str] = data.get("default_value")
        self.title: str = data.get("title")


class ButtonStringPicker:
    def __init__(self, data: dict):
        self.items: List[str] = data.get("items", [])
        self.default_value: Optional[str] = data.get("default_value")
        self.title: Optional[str] = data.get("title")


class ButtonCalendar:
    def __init__(self, data: dict):
        self.default_value: Optional[str] = data.get("default_value")
        self.type: str = data.get("type")
        self.min_year: str = data.get("min_year")
        self.max_year: str = data.get("max_year")
        self.title: str = data.get("title")


class ButtonLocation:
    def __init__(self, data: dict):
        self.default_pointer_location = Location(data.get("default_pointer_location", {}))
        self.default_map_location = Location(data.get("default_map_location", {}))
        self.type: str = data.get("type")
        self.title: Optional[str] = data.get("title")
        self.location_image_url: str = data.get("location_image_url")


class ButtonSelectionItem:
    def __init__(self, data: dict):
        self.text: str = data.get("text")
        self.image_url: str = data.get("image_url")
        self.type: str = data.get("type")


class ButtonSelection:
    def __init__(self, data: dict):
        self.selection_id: str = data.get("selection_id")
        self.search_type: str = data.get("search_type")
        self.get_type: str = data.get("get_type")
        self.items: List[ButtonSelectionItem] = [ButtonSelectionItem(i) for i in data.get("items", [])]
        self.is_multi_selection: bool = data.get("is_multi_selection")
        self.columns_count: str = data.get("columns_count")
        self.title: str = data.get("title")


class Button:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: str = data.get("type")
        self.button_text: str = data.get("button_text")
        self.button_selection = ButtonSelection(data.get("button_selection", {})) if "button_selection" in data else None
        self.button_calendar = ButtonCalendar(data.get("button_calendar", {})) if "button_calendar" in data else None
        self.button_number_picker = ButtonNumberPicker(data.get("button_number_picker", {})) if "button_number_picker" in data else None
        self.button_string_picker = ButtonStringPicker(data.get("button_string_picker", {})) if "button_string_picker" in data else None
        self.button_location = ButtonLocation(data.get("button_location", {})) if "button_location" in data else None
        self.button_textbox = ButtonTextbox(data.get("button_textbox", {})) if "button_textbox" in data else None


class KeypadRow:
    def __init__(self, data: dict):
        self.buttons: List[Button] = [Button(btn) for btn in data.get("buttons", [])]


class Keypad:
    def __init__(self, data: dict):
        self.rows: List[KeypadRow] = [KeypadRow(r) for r in data.get("rows", [])]
        self.resize_keyboard: bool = data.get("resize_keyboard", False)
        self.on_time_keyboard: bool = data.get("on_time_keyboard", False)


class Chat:
    def __init__(self, data: dict):
        self.chat_id: str = data.get("chat_id")
        self.chat_type: str = data.get("chat_type")
        self.user_id: str = data.get("user_id")
        self.first_name: str = data.get("first_name")
        self.last_name: str = data.get("last_name")
        self.title: str = data.get("title")
        self.username: str = data.get("username")


class Bot:
    def __init__(self, data: dict):
        self.bot_id: str = data.get("bot_id")
        self.bot_title: str = data.get("bot_title")
        self.avatar = File(data.get("avatar", {}))
        self.description: str = data.get("description")
        self.username: str = data.get("username")
        self.start_message: str = data.get("start_message")
        self.share_url: str = data.get("share_url")

class hybrid_property:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        coro = self.func(instance)
        try:
            loop = asyncio.get_running_loop()
            return coro
        except RuntimeError:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
class Message:
    def __init__(self, bot, chat_id, message_id, sender_id, text=None, raw_data=None):
        self.bot = bot
        self.raw_data = raw_data or {}
        self.chat_id = chat_id
        self.object_guid = chat_id
        self.author_guid  = self.raw_data.get("sender_id", sender_id)
        self.message_id: str = self.raw_data.get("message_id", message_id)
        self.text: str = self.raw_data.get("text", text)
        self.has_link = contains_link_or_mention(self.raw_data.get("text", text))
        self.is_link = self.has_link
        self.is_mention = bool(re.search(r"@\w+", self.raw_data.get("text", text) or ""))
        self.is_hashtag = bool(re.search(r"#\w+", text or ""))
        self.is_number = bool(re.search(r"\d+", text or ""))
        self.is_emoji = contains_emoji(self.raw_data.get("text", text))
        self.emoji_count = count_emojis(self.raw_data.get("text", text))
        self.is_pure_emoji = bool(self.is_emoji and self.emoji_count == len(self.text))
        self.is_photo = None
        self.is_video = None
        self.is_audio = None
        self.is_voice = None
        self.is_document = None
        self.is_archive = None
        self.is_executable = None
        self.is_font = None
        self.metadata = self.raw_data.get("metadata", {})
        self.is_metadata = self.metadata
        self.meta_parts = self.metadata.get("meta_data_parts", [])
        self.has_metadata = bool(self.meta_parts)
        self.meta_types = [part.get("type") for part in self.meta_parts] if self.has_metadata else []
        self.is_bold = "Bold" in self.meta_types
        self.is_italic = "Italic" in self.meta_types
        self.is_strike = "Strike" in self.meta_types
        self.is_underline = "Underline" in self.meta_types
        self.is_quote = "Quote" in self.meta_types
        self.is_spoiler = "Spoiler" in self.meta_types
        self.is_pre = "Pre" in self.meta_types
        self.is_mono = "Mono" in self.meta_types
        self.is_link_meta = "Link" in self.meta_types
        self.meta_links = [part.get("link_url") for part in self.meta_parts if part.get("type") == "Link"]
        self.meta_link_positions = [
            {"from": part.get("from_index"), "length": part.get("length"), "url": part.get("link_url")}
            for part in self.meta_parts if part.get("type") == "Link"
        ]
        self.has_link = contains_link_or_mention(self.text) or self.is_link_meta
        self.is_formatted = any([
            self.is_bold,
            self.is_italic,
            self.is_strike,
            self.is_underline,
            self.is_quote,
            self.is_spoiler,
            self.is_pre,
            self.is_mono
        ])
        self.sender_id: str = self.raw_data.get("sender_id", sender_id)
        self.time: str = self.raw_data.get("time")
        self.is_edited: bool = self.raw_data.get("is_edited", False)
        self.sender_type: str = self.raw_data.get("sender_type")
        self.args = []
        self.is_command = bool(self.text and self.text.startswith("/"))
        self.is_user = self.chat_id.startswith("b")
        self.is_private = self.chat_id.startswith("b")
        self.is_group = self.chat_id.startswith("g")
        self.is_channel = self.chat_id.startswith("c")
        self.reply_to_message_id: Optional[str] = self.raw_data.get("reply_to_message_id")
        self.forwarded_from = ForwardedFrom(self.raw_data["forwarded_from"]) if "forwarded_from" in self.raw_data else None
        self.file = File(self.raw_data["file"]) if "file" in self.raw_data else None
        self.sticker = Sticker(self.raw_data["sticker"]) if "sticker" in self.raw_data else None
        self.contact_message = ContactMessage(self.raw_data["contact_message"]) if "contact_message" in self.raw_data else None
        self.poll = Poll(self.raw_data["poll"]) if "poll" in self.raw_data else None
        self.location = Location(self.raw_data["location"]) if "location" in self.raw_data else None
        self.live_location = LiveLocation(self.raw_data["live_location"]) if "live_location" in self.raw_data else None
        self.aux_data = AuxData(self.raw_data["aux_data"]) if "aux_data" in self.raw_data else None
        self.is_reply = self.reply_to_message_id is not None
        self.has_media = any([self.file, self.sticker, self.poll, self.location, self.live_location])
        self.is_forwarded = self.forwarded_from is not None
        self.is_text = bool(self.text and not self.has_media)
        self.is_media = self.has_media
        self.is_poll = self.poll is not None
        self.is_location = self.location is not None
        self.is_live_location = self.live_location is not None
        self.is_contact = self.contact_message is not None
        self.has_any_media = any([self.file, self.sticker, self.poll, self.location, self.live_location])
        self.edited_text = self.raw_data.get("edited_text") if self.is_edited else None
        if self.file and self.file.file_name:
            name = self.file.file_name.lower()
            self.is_photo = name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
            self.is_video = name.endswith((".mp4", ".mov", ".avi", ".mkv", ".webm"))
            self.is_audio = name.endswith((".mp3", ".wav", ".ogg", ".m4a", ".flac"))
            self.is_voice = name.endswith((".ogg", ".m4a"))
            self.is_document = name.endswith((".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"))
            self.is_archive = name.endswith((".zip", ".rar", ".7z", ".tar", ".gz"))
            self.is_executable = name.endswith((".exe", ".msi", ".bat", ".sh"))
            self.is_font = name.endswith((".ttf", ".otf", ".woff", ".woff2"))
    @property
    def session(self):
        if self.chat_id not in self.bot.sessions:
            self.bot.sessions[self.chat_id] = {}
        return self.bot.sessions[self.chat_id]
    
    def reply(self, text: str, delete_after: int = None,parse_mode : Optional[Literal["HTML", "Markdown"]] = None , **kwargs):
        async def _reply_async():
            send_func = self.bot.send_message
            if inspect.iscoroutinefunction(send_func):
                msg = await send_func(
                    self.chat_id,
                    text,
                    reply_to_message_id=self.message_id,
                    delete_after=delete_after,
                    parse_mode=parse_mode,
                    **kwargs
                )
            else:
                msg = send_func(
                    self.chat_id,
                    text,
                    reply_to_message_id=self.message_id,
                    delete_after=delete_after,
                    **kwargs
                )
            class Pick:
                def __init__(self, bot, chat_id, message_id):
                    self.bot = bot
                    self.chat_id = chat_id
                    self.message_id = message_id

                def edit(self, new_text):
                    async def _edit():
                        func = self.bot.edit_message_text
                        if inspect.iscoroutinefunction(func):
                            await func(self.chat_id, self.message_id, new_text)
                        else:
                            func(self.chat_id, self.message_id, new_text)

                    try:
                        loop = asyncio.get_running_loop()
                        if loop.is_running():
                            return asyncio.create_task(_edit())
                    except RuntimeError:
                        return asyncio.run(_edit())

                def delete(self):
                    async def _delete():
                        func = self.bot.delete_message
                        if inspect.iscoroutinefunction(func):
                            await func(self.chat_id, self.message_id)
                        else:
                            func(self.chat_id, self.message_id)
                    try:
                        loop = asyncio.get_running_loop()
                        if loop.is_running():
                            return asyncio.create_task(_delete())
                    except RuntimeError:
                        return asyncio.run(_delete())
            chat_id = msg.get("chat_id") if isinstance(msg, dict) else getattr(msg, "chat_id", self.chat_id)
            message_id = msg.get("message_id") if isinstance(msg, dict) else getattr(msg, "message_id", self.message_id)
            return Pick(self.bot, chat_id, message_id)
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                return asyncio.create_task(_reply_async())
        except RuntimeError:
            return asyncio.run(_reply_async())
    def answer(self, text: str, **kwargs):
        return self.bot.send_message(
            self.chat_id,
            text,
            reply_to_message_id=self.message_id,
            **kwargs
        )
    

    def reply_poll(
        self,
        question: str,
        options: List[str],
        type: Literal['Regular', 'Quiz'] = "Regular",
        allows_multiple_answers: bool = False,
        is_anonymous: bool = True,
        correct_option_index: Optional[int] = None,
        hint: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        show_results: bool = False,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[Literal['New', 'Remove', 'None']] = None,
        **kwargs
    ) -> dict:
        payload = {
            "chat_id": self.chat_id,
            "question": question,
            "options": options,
            "type": type,
            "allows_multiple_answers": allows_multiple_answers,
            "is_anonymous": is_anonymous,
            "correct_option_index": correct_option_index,
            "hint": hint,
            "reply_to_message_id": self.message_id if not reply_to_message_id else reply_to_message_id,
            "disable_notification": disable_notification,
            "show_results": show_results,
            "inline_keypad": inline_keypad,
            "chat_keypad": chat_keypad,
            "chat_keypad_type": chat_keypad_type,
        }
        return self.bot._post("sendPoll", {key: value for key, value in payload.items() if value is not None}, **kwargs)
    

    def reply_document(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":chat_keypad_type == "New"
        return self.bot.send_document(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )
    def reply_file(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"

        return self.bot.send_document(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_image(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_image(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_music(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_music(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_voice(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_voice(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_gif(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":chat_keypad_type == "New"
        return self.bot.send_gif(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_location(self, latitude: str, longitude: str, **kwargs) -> Dict[str, Any]:
        return self.bot.send_location(
            chat_id=self.chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_contact(self, first_name: str, last_name: str, phone_number: str, **kwargs) -> Dict[str, Any]:
        return self.bot.send_contact(
            chat_id=self.chat_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_keypad(self, text: str, keypad: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            chat_keypad_type="New",
            chat_keypad=keypad,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_inline(self, text: str, inline_keypad: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            inline_keypad=inline_keypad,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_sticker(self, sticker_id: str, **kwargs) -> Dict[str, Any]:
        return self.bot._post("sendSticker", {
            "chat_id": self.chat_id,
            "sticker_id": sticker_id,
            "reply_to_message_id": self.message_id,
            **kwargs
        })

    def edit(self, new_text: str) -> Dict[str, Any]:
        return self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=new_text
        )

    def delete(self) -> Dict[str, Any]:
        return self.bot.delete_message(
            chat_id=self.chat_id,
            message_id=self.message_id
        )
    @hybrid_property
    async def author_name(self):return await self.bot.get_name(self.chat_id)
    @hybrid_property
    async def name(self):return await self.bot.get_name(self.chat_id)
    @hybrid_property
    async def username(self):return await self.bot.get_username(self.chat_id)
    @hybrid_property
    async def author_info(self):return await self.bot.get_chat(self.chat_id)
class AuxData:
    def __init__(self, data: dict):
        self.start_id = data.get("start_id")
        self.button_id = data.get("button_id")


class InlineMessage:
    def __init__(self, bot, raw_data: dict):
        self.bot = bot
        self.raw_data = raw_data
        chat_id : str = raw_data.get("chat_id")
        sender_id : str = raw_data.get("sender_id")
        self.chat_id: str = raw_data.get("chat_id")
        self.message_id: str = raw_data.get("message_id")
        self.sender_id: str = raw_data.get("sender_id")
        self.text: str = raw_data.get("text")
        self.aux_data = AuxData(raw_data.get("aux_data", {})) if "aux_data" in raw_data else None
        self.bot = bot
        self.raw_data = raw_data or {}
        self.object_guid = chat_id
        self.author_guid  = self.raw_data.get("sender_id", sender_id)
        self.has_link = bool(re.search(r"(https?://[^\s]+ | www\.[^\s]+ | [a-zA-Z0-9.-]+\.(com|net|org|ir|edu|gov|info|biz|io|me|co) | t\.me/[^\s]+ | telegram\.me/[^\s]+ | @\w+ | \b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)", self.text))
        self.sender_id: str = self.raw_data.get("sender_id", sender_id)
        self.time: str = self.raw_data.get("time")
        self.is_edited: bool = self.raw_data.get("is_edited", False)
        self.sender_type: str = self.raw_data.get("sender_type")
        self.args = []
        self.is_command = bool(self.text and self.text.startswith("/"))
        self.is_user = self.chat_id.startswith("b")
        self.is_private = self.chat_id.startswith("b")
        self.is_group = self.chat_id.startswith("g")
        self.is_channel = self.chat_id.startswith("c")
        self.reply_to_message_id: Optional[str] = self.raw_data.get("reply_to_message_id")
        self.forwarded_from = ForwardedFrom(self.raw_data["forwarded_from"]) if "forwarded_from" in self.raw_data else None
        self.file = File(self.raw_data["file"]) if "file" in self.raw_data else None
        self.sticker = Sticker(self.raw_data["sticker"]) if "sticker" in self.raw_data else None
        self.contact_message = ContactMessage(self.raw_data["contact_message"]) if "contact_message" in self.raw_data else None
        self.aux_data = AuxData(self.raw_data["aux_data"]) if "aux_data" in self.raw_data else None
        self.is_reply = self.reply_to_message_id is not None
        self.has_media = any([self.file, self.sticker])
        self.is_forwarded = self.forwarded_from is not None
        self.is_text = bool(self.text and not self.has_media)
        self.is_media = self.has_media
        self.is_contact = self.contact_message is not None
        self.has_any_media = any([self.file, self.sticker,])
        self.edited_text = self.raw_data.get("edited_text") if self.is_edited else None
        if self.file and self.file.file_name:
            name = self.file.file_name.lower()
            self.is_photo = name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
            self.is_video = name.endswith((".mp4", ".mov", ".avi", ".mkv", ".webm"))
            self.is_audio = name.endswith((".mp3", ".wav", ".ogg", ".m4a", ".flac"))
            self.is_voice = name.endswith((".ogg", ".m4a"))
            self.is_document = name.endswith((".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"))
            self.is_archive = name.endswith((".zip", ".rar", ".7z", ".tar", ".gz"))
            self.is_executable = name.endswith((".exe", ".msi", ".bat", ".sh"))
            self.is_font = name.endswith((".ttf", ".otf", ".woff", ".woff2"))
        

    @property
    def session(self):
        if self.chat_id not in self.bot.sessions:
            self.bot.sessions[self.chat_id] = {}
        return self.bot.sessions[self.chat_id]
    
    def reply(self, text: str, delete_after: int = None, **kwargs):
        async def _reply_async():
            send_func = self.bot.send_message
            if inspect.iscoroutinefunction(send_func):
                msg = await send_func(
                    self.chat_id,
                    text,
                    reply_to_message_id=self.message_id,
                    delete_after=delete_after,
                    **kwargs
                )
            else:
                msg = send_func(
                    self.chat_id,
                    text,
                    reply_to_message_id=self.message_id,
                    delete_after=delete_after,
                    **kwargs
                )
            class Pick:
                def __init__(self, bot, chat_id, message_id):
                    self.bot = bot
                    self.chat_id = chat_id
                    self.message_id = message_id

                def edit(self, new_text):
                    async def _edit():
                        func = self.bot.edit_message_text
                        if inspect.iscoroutinefunction(func):
                            await func(self.chat_id, self.message_id, new_text)
                        else:
                            func(self.chat_id, self.message_id, new_text)

                    try:
                        loop = asyncio.get_running_loop()
                        if loop.is_running():
                            return asyncio.create_task(_edit())
                    except RuntimeError:
                        return asyncio.run(_edit())

                def delete(self):
                    async def _delete():
                        func = self.bot.delete_message
                        if inspect.iscoroutinefunction(func):
                            await func(self.chat_id, self.message_id)
                        else:
                            func(self.chat_id, self.message_id)
                    try:
                        loop = asyncio.get_running_loop()
                        if loop.is_running():
                            return asyncio.create_task(_delete())
                    except RuntimeError:
                        return asyncio.run(_delete())
            chat_id = msg.get("chat_id") if isinstance(msg, dict) else getattr(msg, "chat_id", self.chat_id)
            message_id = msg.get("message_id") if isinstance(msg, dict) else getattr(msg, "message_id", self.message_id)
            return Pick(self.bot, chat_id, message_id)
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                return asyncio.create_task(_reply_async())
        except RuntimeError:
            return asyncio.run(_reply_async())
    def answer(self, text: str, **kwargs):
        return self.bot.send_message(
            self.chat_id,
            text,
            reply_to_message_id=self.message_id,
            **kwargs
        )
    

    def reply_poll(self, question: str, options: List[str], **kwargs) -> Dict[str, Any]:
        return self.bot._post("sendPoll", {
            "chat_id": self.chat_id,
            "question": question,
            "options": options,
            "reply_to_message_id": self.message_id,
            **kwargs
        })
    

    def reply_document(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":chat_keypad_type == "New"
        return self.bot.send_document(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )
    def reply_file(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"

        return self.bot.send_document(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_image(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_image(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_music(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_music(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_voice(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":
            chat_keypad_type == "New"
        return self.bot.send_voice(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_gif(
        self,
        path: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        chat_keypad_type: Optional[str] = "None",
        disable_notification: bool = False
    ):
        if chat_keypad and chat_keypad_type == "none":chat_keypad_type == "New"
        return self.bot.send_gif(
            chat_id=self.chat_id,
            path=path,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            chat_keypad_type=chat_keypad_type,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id
        )

    def reply_location(self, latitude: str, longitude: str, **kwargs) -> Dict[str, Any]:
        return self.bot.send_location(
            chat_id=self.chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_contact(self, first_name: str, last_name: str, phone_number: str, **kwargs) -> Dict[str, Any]:
        return self.bot.send_contact(
            chat_id=self.chat_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_keypad(self, text: str, keypad: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            chat_keypad_type="New",
            chat_keypad=keypad,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_inline(self, text: str, inline_keypad: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            inline_keypad=inline_keypad,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def reply_sticker(self, sticker_id: str, **kwargs) -> Dict[str, Any]:
        return self.bot._post("sendSticker", {
            "chat_id": self.chat_id,
            "sticker_id": sticker_id,
            "reply_to_message_id": self.message_id,
            **kwargs
        })

    def edit(self, new_text: str) -> Dict[str, Any]:
        return self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=new_text
        )

    def delete(self) -> Dict[str, Any]:
        return self.bot.delete_message(
            chat_id=self.chat_id,
            message_id=self.message_id
        )
    @hybrid_property
    async def author_name(self):return await self.bot.get_name(self.chat_id)
    @hybrid_property
    async def name(self):return await self.bot.get_name(self.chat_id)
    @hybrid_property
    async def username(self):return await self.bot.get_username(self.chat_id)
    @hybrid_property
    async def author_info(self):return await self.bot.get_chat(self.chat_id)