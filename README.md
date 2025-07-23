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

# 📦 Rubka `Message` Class & Media Reply API Documentation

## 🧾 معرفی کلاس `Message`

کلاس `Message` در کتابخانه Rubka ابزاری کلیدی برای مدیریت پیام‌های دریافتی در ربات است. این کلاس، قابلیت‌هایی همچون پاسخ به پیام، ارسال مدیا، حذف یا ویرایش پیام، و استفاده از صفحه‌کلید و دکمه‌های اینلاین را فراهم می‌کند.

---

## ⚙️ مشخصات کلاس `Message`

```python
Message(bot, chat_id, message_id, sender_id, text=None, raw_data=None)
```

### پارامترها:

| پارامتر      | توضیح                                    |
| ------------ | ---------------------------------------- |
| `bot`        | نمونه‌ی شی ربات                          |
| `chat_id`    | شناسه چت                                 |
| `message_id` | آیدی پیام                                |
| `sender_id`  | شناسه فرستنده                            |
| `text`       | متن پیام                                 |
| `raw_data`   | داده‌ی خام پیام (دیکشنری دریافتی از API) |

### ویژگی‌ها (Attributes):

- `reply_to_message_id` – اگر پیام در پاسخ ارسال شده باشد، آیدی پیام اولیه
- `file`, `sticker`, `poll`, `contact_message`, `location`, ... – داده‌های مربوطه اگر وجود داشته باشند

---

## 📩 متدهای پاسخ‌دهی

### ✉️ `reply(text: str, **kwargs)`

پاسخ متنی به پیام با قابلیت ارسال دکمه و گزینه‌های اضافی.

### 📊 `reply_poll(question, options, **kwargs)`

ارسال نظرسنجی در پاسخ به پیام.

### 📎 `reply_document(...)`

ارسال فایل یا سند با متن اختیاری و دکمه.

### 🖼 `reply_image(...)`

ارسال تصویر با قابلیت reply همراه دکمه‌های chat یا inline.

### 🎵 `reply_music(...)`

ارسال موزیک در پاسخ.

### 🎤 `reply_voice(...)`

ارسال پیام صوتی (voice).

### 🎞 `reply_gif(...)`

ارسال گیف در پاسخ به پیام.

### 🗺 `reply_location(latitude, longitude, **kwargs)`

ارسال لوکیشن در پاسخ.

### 📇 `reply_contact(first_name, last_name, phone_number, **kwargs)`

ارسال مخاطب در پاسخ.

---

## 🔘 پاسخ با دکمه‌ها

### `reply_keypad(text, keypad, **kwargs)`

ارسال پیام با صفحه‌کلید چتی (ChatKeypad).

### `reply_inline(text, inline_keypad, **kwargs)`

ارسال پیام با دکمه‌های شیشه‌ای (Inline).

---

## 📦 پاسخ با فایل‌ها و استیکر

### `reply_sticker(sticker_id, **kwargs)`

ارسال استیکر در پاسخ به پیام.

### `reply_file(file_id, **kwargs)`

ارسال فایل بر اساس File ID.

---

## ✏️ ویرایش و حذف

### `edit(new_text)`

ویرایش متن پیام.

### `delete()`

حذف پیام فعلی.

---

## 📤 مثال کاربردی کامل

```python
@bot.on_message()
def handler(bot: Robot, message: Message):
    # پاسخ با تصویر و دکمه‌های مختلف
    message.reply_image(
        path="https://s6.uupload.ir/files/sample.png",
        text="📷 تصویر پاسخ‌داده‌شده با دکمه‌ها",
        inline_keypad=inline_keypad
    )

    message.reply_image(
        path="https://s6.uupload.ir/files/sample.png",
        text="📷 تصویر دوم با صفحه‌کلید",
        chat_keypad=chat_keypad,
        chat_keypad_type="New"
    )

@bot.on_callback()
def callback_handler(bot: Robot, message: Message):
    data = message.aux_data.button_id
    if data == "btn_male":
        message.reply("سلام آقا 👨")
    elif data == "btn_female":
        message.reply("سلام خانم 👩")
    else:
        message.reply(f"دکمه ناشناخته: {data}")
```

---

## 🧠 نکته

تمامی متدهای `reply_*` به‌صورت خودکار پیام جدید را در پاسخ به پیام اصلی ارسال می‌کنند (`reply_to_message_id` به‌صورت داخلی تنظیم می‌شود).

---

---

## 📤 مثال کاربردی کامل

```python
from rubka import Robot
from rubka.keypad import ChatKeypadBuilder
from rubka.button import InlineBuilder
from rubka.context import Message

chat_keypad = ChatKeypadBuilder().row(
    ChatKeypadBuilder().button(id="btn_female", text="زن"),
    ChatKeypadBuilder().button(id="btn_male", text="مرد")
).build()

inline_keypad = (
    InlineBuilder()
    .row(
        InlineBuilder().button_simple("btn_bets", "button1"),
        InlineBuilder().button_simple("btn_rps", "button2")
    )
    .row(
        InlineBuilder().button_simple("btn_chatid", "butthon3")
    )
    .build()
)

bot = Robot("توکن شما")

@bot.on_message()
def handler(bot: Robot, message: Message):
    message.reply_image(
        path="https://s6.uupload.ir/files/chatgpt_image_jul_20,_2025,_10_22_47_pm_oiql.png",
        text="📷 عکس ریپلای شده دکمه شیشه ای",
        inline_keypad=inline_keypad
    )

    message.reply_image(
        path="https://s6.uupload.ir/files/chatgpt_image_jul_20,_2025,_10_22_47_pm_oiql.png",
        text="📷 عکس ریپلای شده دکمه کیبوردی",
        chat_keypad=chat_keypad,
        chat_keypad_type="New"
    )

@bot.on_callback()
def callback_handler(bot: Robot, message: Message):
    data = message.aux_data.button_id
    if data == "btn_male":
        message.reply("سلام مرد")
    elif data == "btn_female":
        message.reply("سلام زن")
    else:
        message.reply(f"دکمه ناشناخته: {data}")

bot.run()
```

---

## 🧱 مستندات کلاس `InlineBuilder`

کلاس `InlineBuilder` برای ساخت دکمه‌های اینلاین استفاده می‌شود که در پیام‌های ربات قابل استفاده هستند.

### ✅ روش استفاده

```python
from rubka.button import InlineBuilder

builder = InlineBuilder()
inline_keypad = builder.row(
    builder.button_simple("btn_1", "دکمه ۱"),
    builder.button_simple("btn_2", "دکمه ۲")
).build()
```

### 📚 دکمه‌های پشتیبانی‌شده

- `button_simple(id, text)` – دکمه ساده
- `button_payment(id, title, amount, description=None)` – پرداخت
- `button_calendar(id, title, type_, ...)` – انتخاب تاریخ
- `button_location(id, type_, image_url, ...)` – ارسال موقعیت مکانی
- `button_string_picker(...)` – انتخاب گزینه از لیست
- `button_number_picker(...)` – انتخاب عدد از بازه
- `button_textbox(...)` – فیلد ورود متنی
- `button_selection(...)` – انتخاب چندگزینه‌ای پیشرفته
- `button_camera_image(...)`, `button_camera_video(...)`
- `button_gallery_image(...)`, `button_gallery_video(...)`
- `button_file(...)`, `button_audio(...)`, `button_record_audio(...)`
- `button_my_phone_number(...)`, `button_my_location(...)`
- `button_ask_my_phone_number(...)`, `button_ask_location(...)`
- `button_barcode(...)`
- `button_link(id, title, url)` – لینک خارجی

### 🧱 ساخت نهایی

```python
keypad = builder.build()
```

خروجی به صورت دیکشنری با کلید `rows` خواهد بود که می‌توانید در متد `send_message` یا `reply_*` استفاده کنید.

---

## ⌨️ مستندات کلاس `ChatKeypadBuilder`

کلاس `ChatKeypadBuilder` برای ساخت صفحه‌کلید چتی (chat keypad) استفاده می‌شود.

### 🛠 روش استفاده

```python
from rubka.keypad import ChatKeypadBuilder

keypad = ChatKeypadBuilder().row(
    ChatKeypadBuilder().button("btn_1", "دکمه ۱"),
    ChatKeypadBuilder().button("btn_2", "دکمه ۲")
).build()
```

### 📋 متدها

- `button(id, text, type="Simple")` – ساخت یک دکمه ساده یا از نوع خاص
- `row(*buttons)` – افزودن یک ردیف به کیبورد (دکمه‌ها باید با `button()` ساخته شوند)
- `build(resize_keyboard=True, on_time_keyboard=False)` – ساخت خروجی نهایی برای ارسال به کاربر

### 📦 خروجی `build()`

```json
{
  "rows": [
    {"buttons": [
      {"id": "btn_1", "type": "Simple", "button_text": "دکمه ۱"},
      {"id": "btn_2", "type": "Simple", "button_text": "دکمه ۲"}
    ]}
  ],
  "resize_keyboard": true,
  "on_time_keyboard": false
}
```

---

## 👨‍💻 توسعه‌دهنده

این مستندات برای کتابخانه `rubka` توسط **Codern Team** تهیه شده است.

📎 لینک: [https://api-free.ir](https://api-free.ir)




