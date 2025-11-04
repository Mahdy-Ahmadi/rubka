from typing import Callable
import re
class TextFilter:
    def __call__(self, keyword=None):
        if keyword is None:
            return Filter(lambda m: getattr(m, "is_text", False))
        else:
            return Filter(lambda m: getattr(m, "is_text", False) and keyword in getattr(m, "text", ""))
class Filter:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, message):
        return self.func(message)

    def __and__(self, other):
        return Filter(lambda m: self(m) and other(m))

    def __or__(self, other):
        return Filter(lambda m: self(m) or other(m))

    def __invert__(self):
        return Filter(lambda m: not self(m))

    def __xor__(self, other):
        return Filter(lambda m: self(m) != other(m))

    def __eq__(self, other):
        return Filter(lambda m: self(m) == other)

    def __ne__(self, other):
        return Filter(lambda m: self(m) != other)

    def __lt__(self, other):
        return Filter(lambda m: self(m) < other)

    def __le__(self, other):
        return Filter(lambda m: self(m) <= other)

    def __gt__(self, other):
        return Filter(lambda m: self(m) > other)

    def __ge__(self, other):
        return Filter(lambda m: self(m) >= other)

    def __add__(self, other):
        return Filter(lambda m: self(m) + (other(m) if callable(other) else other))

    def __sub__(self, other):
        return Filter(lambda m: self(m) - (other(m) if callable(other) else other))

    def __mul__(self, other):
        return Filter(lambda m: self(m) * (other(m) if callable(other) else other))

    def __truediv__(self, other):
        return Filter(lambda m: self(m) / (other(m) if callable(other) else other))
class IsCommand(Filter):
    def __init__(self, commands=None):
        if commands is None:
            func = lambda m: getattr(m, "is_command", False)
        else:
            if isinstance(commands, str):
                commands = [commands]
            func = lambda m: getattr(m, "is_command", False) and getattr(m, "text", "").lstrip("/").split()[0] in commands

        super().__init__(func)

    def __getattr__(self, name: str):
        return IsCommand([name])


class IsText:
    def __call__(self, text=None):
        if text is None:
            func = lambda m: m.is_text is True and m.is_file is False
        else:
            if isinstance(text, str):
                text = [text]
            func = lambda m: m.is_text is True and m.is_file is False and m.text in text

        return Filter(func)
#is_text = Filter(lambda m: getattr(m, "is_text", False))
is_file = Filter(lambda m: getattr(m, "file", None) is not None)
is_sticker = Filter(lambda m: getattr(m, "sticker", None) is not None)
is_contact = Filter(lambda m: getattr(m, "contact_message", None) is not None)
is_poll = Filter(lambda m: getattr(m, "poll", None) is not None)
is_location = Filter(lambda m: getattr(m, "location", None) is not None)
is_live_location = Filter(lambda m: getattr(m, "live_location", None) is not None)
has_any_media = Filter(lambda m: getattr(m, "has_any_media", False))
has_media = Filter(lambda m: getattr(m, "has_media", False))
is_text = IsText()
is_command = IsCommand()
is_user = Filter(lambda m: getattr(m, "is_user", False))
is_private = Filter(lambda m: getattr(m, "is_private", False))
is_group = Filter(lambda m: getattr(m, "is_group", False))
is_channel = Filter(lambda m: getattr(m, "is_channel", False))
is_reply = Filter(lambda m: getattr(m, "is_reply", False))
is_forwarded = Filter(lambda m: getattr(m, "is_forwarded", False))
is_edited = Filter(lambda m: getattr(m, "is_edited", False))
def text(keyword: str):
    return Filter(lambda m: getattr(m, "text", "") and keyword in m.text)
def text_length(min_len: int = 0, max_len: int = None):
    def _filter(m):
        t = getattr(m, "text", "")
        if not t: return False
        if len(t) < min_len: return False
        if max_len is not None and len(t) > max_len: return False
        return True
    return Filter(_filter)
def text_regex(pattern: str):
    regex = re.compile(pattern)
    return Filter(lambda m: getattr(m, "text", "") and regex.search(m.text))
def text_startswith(prefix: str):
    return Filter(lambda m: getattr(m, "text", "").startswith(prefix) if getattr(m, "text", None) else False)
def text_endswith(suffix: str):
    return Filter(lambda m: getattr(m, "text", "").endswith(suffix) if getattr(m, "text", None) else False)
def text_upper():
    return Filter(lambda m: getattr(m, "text", "").isupper() if getattr(m, "text", None) else False)
def text_lower():
    return Filter(lambda m: getattr(m, "text", "").islower() if getattr(m, "text", None) else False)
def text_digit():
    return Filter(lambda m: getattr(m, "text", "").isdigit() if getattr(m, "text", None) else False)
def text_word_count(min_words: int = 1, max_words: int = None):
    def _filter(m):
        t = getattr(m, "text", "")
        if not t: return False
        wc = len(t.split())
        if wc < min_words: return False
        if max_words is not None and wc > max_words: return False
        return True
    return Filter(_filter)
def text_contains_any(keywords: list):
    return Filter(lambda m: getattr(m, "text", "") and any(k in m.text for k in keywords))
def text_equals(value: str):
    return Filter(lambda m: getattr(m, "text", None) == value)
def text_not_equals(value: str):
    return Filter(lambda m: getattr(m, "text", None) != value)
def file_size_gt(size: int):
    return Filter(lambda m: m.file and getattr(m.file, "size", 0) > size)
def file_size_lt(size: int):
    return Filter(lambda m: m.file and getattr(m.file, "size", 0) < size)
def file_name_contains(substring: str):
    return Filter(lambda m: m.file and substring in getattr(m.file, "file_name", ""))
def file_extension(ext: str):
    return Filter(lambda m: m.file and getattr(m.file, "file_name", "").endswith(ext))
def file_id_is(file_id: str):
    return Filter(lambda m: m.file and getattr(m.file, "file_id", None) == file_id)
def sticker_id_is(sid: str):
    return Filter(lambda m: m.sticker and getattr(m.sticker, "sticker_id", None) == sid)
def sticker_emoji_is(emoji: str):
    return Filter(lambda m: m.sticker and getattr(m.sticker, "emoji", None) == emoji)
def poll_question_contains(keyword: str):
    return Filter(lambda m: m.poll and keyword in getattr(m.poll, "question", ""))
def poll_option_count(min_options: int = 1, max_options: int = None):
    def _filter(m):
        if not getattr(m, "poll", None): return False
        options = getattr(m.poll, "options", [])
        if len(options) < min_options: return False
        if max_options is not None and len(options) > max_options: return False
        return True
    return Filter(_filter)
def location_within(lat_min, lat_max, long_min, long_max):
    def _filter(m):
        loc = getattr(m, "location", None)
        if not loc: return False
        return lat_min <= getattr(loc, "lat", 0) <= lat_max and long_min <= getattr(loc, "long", 0) <= long_max
    return Filter(_filter)
def live_location_within(lat_min, lat_max, long_min, long_max):
    def _filter(m):
        loc = getattr(m, "live_location", None)
        if not loc: return False
        return lat_min <= getattr(loc, "lat", 0) <= lat_max and long_min <= getattr(loc, "long", 0) <= long_max
    return Filter(_filter)
def has_media_types(types: list):
    return Filter(lambda m: any(getattr(m, t, None) for t in types))

def message_id_is(mid: str):
    return Filter(lambda m: getattr(m, "message_id", None) == mid)

def is_reply_to_user(user_id: str):
    return Filter(lambda m: getattr(m, "reply_to_message_id", None) == user_id)

def is_forwarded_from(user_id: str):
    return Filter(lambda m: getattr(m.forwarded_from, "sender_id", None) == user_id if getattr(m, "forwarded_from", None) else False)

def edited_text_contains(keyword: str):
    return Filter(lambda m: getattr(m, "edited_text", "") and keyword in m.edited_text)

def aux_data_contains(key: str, value):
    return Filter(lambda m: getattr(m.aux_data, key, None) == value if getattr(m, "aux_data", None) else False)




def file_attr(attr_name):
    return Filter(lambda m: m.file and getattr(m.file, attr_name, None))

def sticker_attr(attr_name):
    return Filter(lambda m: m.sticker and getattr(m.sticker, attr_name, None))

def poll_attr(attr_name):
    return Filter(lambda m: m.poll and getattr(m.poll, attr_name, None))

def location_attr(attr_name):
    return Filter(lambda m: m.location and getattr(m.location, attr_name, None))

def live_location_attr(attr_name):
    return Filter(lambda m: m.live_location and getattr(m.live_location, attr_name, None))




file_size = file_attr("size")
file_name = file_attr("file_name")
sticker_id = sticker_attr("sticker_id")
poll_question = poll_attr("question")
location_lat = location_attr("lat")
location_long = location_attr("long")
live_location_lat = live_location_attr("lat")
live_location_long = live_location_attr("long")

_custom_filters = {}
def chat_title_contains(keyword: str):
    
    return Filter(lambda m: getattr(m, "chat", None) and keyword in getattr(m.chat, "title", ""))

def chat_title_equals(value: str):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "title", "") == value)

def chat_id_is(cid: str):
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "id", None) == cid)

def chat_member_count(min_count: int = 0, max_count: int = None):
    
    def _filter(m):
        c = getattr(m, "chat", None)
        if not c: return False
        count = getattr(c, "member_count", 0)
        if count < min_count: return False
        if max_count is not None and count > max_count: return False
        return True
    return Filter(_filter)

def chat_type_is(chat_type: str):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "type", None) == chat_type)

def chat_username_contains(keyword: str):
    
    return Filter(lambda m: getattr(m, "chat", None) and keyword in getattr(m.chat, "username", ""))

def chat_username_equals(value: str):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "username", "") == value)

def chat_has_link():
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "invite_link", None) is not None)

def chat_is_private():
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "type", None) in ["group", "channel"])

def chat_member_count_gt(count: int):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "member_count", 0) > count)

def chat_member_count_lt(count: int):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "member_count", 0) < count)

def chat_has_username():
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "username", None) is not None)

def chat_type_in(types: list):
    
    return Filter(lambda m: getattr(m, "chat", None) and getattr(m.chat, "type", None) in types)


def chat_title_regex(pattern: str):
    regex = re.compile(pattern)
    return Filter(lambda m: getattr(m, "chat", None) and regex.search(getattr(m.chat, "title", "")))

def chat_username_regex(pattern: str):
    regex = re.compile(pattern)
    return Filter(lambda m: getattr(m, "chat", None) and regex.search(getattr(m.chat, "username", "")))
def custom(name):
    def wrapper(func):
        _custom_filters[name] = Filter(func)
        return _custom_filters[name]
    return wrapper

def get_custom(name):
    return _custom_filters.get(name)

def and_(*filters):
    return Filter(lambda m: all(f(m) for f in filters))

def or_(*filters):
    return Filter(lambda m: any(f(m) for f in filters))

def not_(filter_):
    return Filter(lambda m: not filter_(m))