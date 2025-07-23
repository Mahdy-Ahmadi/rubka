# 📚 Rubka Bot Python Library Documentation

## 🧠 Introduction
`rubka` is a Python library to interact with the [Rubika Bot API](https://rubika.ir/). This library helps you create Telegram-like bots with support for messages, inline buttons, chat keypads, and callback handling.

---

## ⚙️ Installation

```bash
pip install rubka
```

If `importlib.metadata` is not available, it installs `importlib-metadata` automatically.

---

## 🚀 Getting Started

```python
from rubka import Robot
from rubka.context import Message

bot = Robot(token="YOUR_TOKEN_HERE")

@bot.on_message(commands=["start"])
def start(bot: Robot, message: Message):
    message.reply("سلام! خوش آمدید!")

bot.run()
```

---

## 📬 Handling Messages

You can handle incoming text messages using `@bot.on_message()`:

```python
@bot.on_message(commands=["hello"])
def greet(bot: Robot, message: Message):
    message.reply("سلام کاربر عزیز 👋")
```

You can also add filters.

---

## 🎮 Handling Callback Buttons

```python
from rubka.keypad import ChatKeypadBuilder

@bot.on_message(commands=["gender"])
def gender(bot: Robot, message: Message):
    keypad = ChatKeypadBuilder().row(
        ChatKeypadBuilder().button(id="male", text="👨 مرد"),
        ChatKeypadBuilder().button(id="female", text="👩 زن")
    ).build()
    message.reply_keypad("جنسیت خود را انتخاب کنید:", keypad)

@bot.on_callback("male")
def on_male(bot: Robot, message: Message):
    message.reply("شما مرد هستید")

@bot.on_callback("female")
def on_female(bot: Robot, message: Message):
    message.reply("شما زن هستید")
```

---

## 🔘 Inline Button Builder

```python
from rubka.button import InlineBuilder

builder = InlineBuilder().row(
    InlineBuilder().button_simple(id="info", text="اطلاعات")
).build()
```

---

## 🔄 Check if User Joined a Channel

```python
channel_guid = "c0xABCDEF..."

@bot.on_message(commands=["check"])
def check(bot: Robot, message: Message):
    if bot.check_join(channel_guid, message.chat_id):
        message.reply("✅ شما عضو کانال هستید")
    else:
        message.reply("❌ لطفاً ابتدا در کانال عضو شوید")
```

---

## 💬 Utility Methods

| Method | Description |
|--------|-------------|
| `get_chat(chat_id)` | دریافت اطلاعات چت |
| `get_name(chat_id)` | دریافت نام کاربر |
| `get_username(chat_id)` | دریافت نام‌کاربری |
| `send_message(...)` | ارسال پیام متنی |
| `edit_message_text(...)` | ویرایش پیام |
| `delete_message(...)` | حذف پیام |
| `send_location(...)` | ارسال موقعیت مکانی |
| `send_poll(...)` | ارسال نظرسنجی |
| `send_contact(...)` | ارسال مخاطب |
| `forward_message(...)` | فوروارد پیام |

---

## 🎛 Inline Query Support

```python
@bot.on_inline_query()
def inline(bot: Robot, message: InlineMessage):
    message.answer("نتیجه اینلاین")
```

---

## 🧱 Button Types

Supported inline button types include:

- `Simple`
- `Payment`
- `Calendar`
- `Location`
- `CameraImage`, `CameraVideo`
- `GalleryImage`, `GalleryVideo`
- `File`, `Audio`, `RecordAudio`
- `MyPhoneNumber`, `MyLocation`
- `Textbox`, `Barcode`, `Link`

See `InlineBuilder` for more.

---

## 🧩 Dynamic Chat Keypad

```python
builder = ChatKeypadBuilder()
keypad = builder.row(
    builder.button(id="play", text="🎮 بازی کن"),
    builder.button(id="exit", text="❌ خروج")
).build()
```

---

## 🧪 Set Commands

```python
bot.set_commands([
    {"command": "start", "description": "شروع"},
    {"command": "help", "description": "راهنما"}
])
```

---

## 🔄 Update Offset Automatically

Bot updates are handled using `get_updates()` and `offset_id` is managed internally.

---

## 🛠 Advanced Features

- `update_bot_endpoint()` – تنظیم webhook یا polling
- `remove_keypad()` – حذف صفحه‌کلید چت
- `edit_chat_keypad()` – ویرایش یا افزودن صفحه‌کلید چت

---

## 👨‍💻 Maintainer

Developed with ❤️ by **Codern Team**.

---

## 🔗 Links

- [Rubika API Docs](https://botapi.rubika.ir)
- [API-Free.ir](https://api-free.ir)
