from typing import Any, Dict, List,Optional

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


# =========================
# Poll
# =========================
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


# =========================
# Location & Contact & ForwardedFrom
# =========================
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


# =========================
# AuxData
# =========================
class AuxData:
    def __init__(self, data: dict):
        self.start_id: str = data.get("start_id")
        self.button_id: str = data.get("button_id")


# =========================
# Button Models
# =========================
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
from typing import Union
from pathlib import Path

class Message:
    def __init__(self, bot, chat_id, message_id, sender_id, text=None, raw_data=None):
        self.bot = bot
        self.chat_id = chat_id
        self.raw_data = raw_data or {}
        self.message_id: str = self.raw_data.get("message_id", message_id)
        self.text: str = self.raw_data.get("text", text)
        self.sender_id: str = self.raw_data.get("sender_id", sender_id)
        self.time: str = self.raw_data.get("time")
        self.is_edited: bool = self.raw_data.get("is_edited", False)
        self.sender_type: str = self.raw_data.get("sender_type")
        self.args = []
        self.reply_to_message_id: Optional[str] = self.raw_data.get("reply_to_message_id")
        self.forwarded_from = ForwardedFrom(self.raw_data["forwarded_from"]) if "forwarded_from" in self.raw_data else None
        self.file = File(self.raw_data["file"]) if "file" in self.raw_data else None
        self.sticker = Sticker(self.raw_data["sticker"]) if "sticker" in self.raw_data else None
        self.contact_message = ContactMessage(self.raw_data["contact_message"]) if "contact_message" in self.raw_data else None
        self.poll = Poll(self.raw_data["poll"]) if "poll" in self.raw_data else None
        self.location = Location(self.raw_data["location"]) if "location" in self.raw_data else None
        self.live_location = LiveLocation(self.raw_data["live_location"]) if "live_location" in self.raw_data else None
        self.aux_data = AuxData(self.raw_data["aux_data"]) if "aux_data" in self.raw_data else None

    @property
    def session(self):
        if self.chat_id not in self.bot.sessions:
            self.bot.sessions[self.chat_id] = {}
        return self.bot.sessions[self.chat_id]
    def reply(self, text: str, **kwargs):
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

    def reply_file(self, file_id: str, **kwargs) -> Dict[str, Any]:
        return self.bot._post("sendFile", {
            "chat_id": self.chat_id,
            "file_id": file_id,
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
class InlineMessage:
    def __init__(self, bot, raw_data: dict):
        self.bot = bot
        self.raw_data = raw_data

        self.chat_id: str = raw_data.get("chat_id")
        self.message_id: str = raw_data.get("message_id")
        self.sender_id: str = raw_data.get("sender_id")
        self.text: str = raw_data.get("text")
        self.aux_data = AuxData(raw_data.get("aux_data", {})) if "aux_data" in raw_data else None

    def reply(self, text: str, **kwargs):
        return self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            reply_to_message_id=self.message_id,
            **kwargs
        )

    def edit(self, new_text: str):
        return self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=new_text
        )

    def delete(self):
        return self.bot.delete_message(
            chat_id=self.chat_id,
            message_id=self.message_id
        )
