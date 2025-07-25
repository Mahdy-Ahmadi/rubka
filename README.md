# 📚 Rubka Bot Python Library Documentation
# نمونه تنظیم وب‌هوک (Webhook) در کتابخونه rubla

برای مشاهده مستندات کامل و آخرین نسخه راهنما، لطفاً به آدرس زیر مراجعه کنید:  
[github.com/Mahdy-Ahmadi](https://github.com/Mahdy-Ahmadi/rubka/blob/main/webhook.md))


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

# 📘 Rubka Bot Method Reference

مستندات مربوط به متدهای اصلی کلاس `Robot` در کتابخانه Rubka.

---

## ✅ پیام‌ها و هندلرها

### `on_message(filters=None, commands=None)`
**توضیح:** ثبت هندلر برای پیام‌های ورودی.
- `filters`: تابع شرطی برای فیلتر پیام‌ها (اختیاری)
- `commands`: لیست دستورهایی که شروع با `/` هستند (اختیاری)

### `on_callback(button_id=None)`
**توضیح:** ثبت هندلر برای دکمه‌های فشرده‌شده
- `button_id`: آیدی دکمه‌ای که باید هندل شود (اختیاری)

### `on_inline_query()`
**توضیح:** ثبت هندلر برای پیام‌های اینلاین (inline query)

---

## 📨 ارسال پیام

### `send_message(...)`
**توضیح:** ارسال پیام متنی به چت
- `chat_id`: آیدی چت مقصد *(str)* ✅
- `text`: محتوای پیام *(str)* ✅
- `chat_keypad`: کی‌پد معمولی *(dict)*
- `inline_keypad`: کی‌پد اینلاین *(dict)*
- `reply_to_message_id`: پاسخ به پیام خاص *(str)*
- `disable_notification`: بدون نوتیف *(bool)*
- `chat_keypad_type`: حالت کی‌پد *("New" | "Removed")*

---

## 📁 ارسال فایل‌ها

### متدهای مشترک (فایل، موزیک، ویس، گیف، عکس):
- `send_document(...)`
- `send_music(...)`
- `send_voice(...)`
- `send_gif(...)`
- `send_image(...)`

**پارامترهای اصلی:**
- `chat_id`: آیدی چت
- `path`: مسیر فایل یا URL (اختیاری)
- `file_id`: اگر فایل قبلاً آپلود شده باشد
- `text`: کپشن فایل
- `file_name`: نام فایل
- `inline_keypad`, `chat_keypad`, `reply_to_message_id`, `disable_notification`, `chat_keypad_type`

---

## 📍 سایر متدهای مهم

### `get_me()`
دریافت اطلاعات ربات

### `get_chat(chat_id)`
دریافت اطلاعات یک چت

### `get_name(chat_id)`
دریافت نام مخاطب بر اساس `first_name` و `last_name`

### `get_username(chat_id)`
دریافت نام کاربری چت (در صورت وجود)

### `check_join(channel_guid, chat_id)`
بررسی عضویت کاربر در کانال خاص

### `remove_keypad(chat_id)`
حذف کی‌پد معمولی چت

### `edit_chat_keypad(chat_id, chat_keypad)`
ویرایش یا اضافه کردن کی‌پد چت

### `edit_message_text(chat_id, message_id, text)`
ویرایش متن پیام ارسال‌شده

### `edit_inline_keypad(chat_id, message_id, inline_keypad)`
ویرایش کی‌پد اینلاین پیام

### `delete_message(chat_id, message_id)`
حذف پیام از چت

### `send_poll(chat_id, question, options)`
ارسال نظرسنجی به چت

### `send_location(chat_id, latitude, longitude, ...)`
ارسال موقعیت مکانی به چت

### `send_contact(chat_id, first_name, last_name, phone_number)`
ارسال مخاطب به چت

### `forward_message(from_chat_id, message_id, to_chat_id)`
فروارد کردن پیام از یک چت به چت دیگر

### `set_commands(bot_commands)`
تنظیم دستورات رسمی ربات (برای `/help` و ...)

### `update_bot_endpoint(url, type)`
تنظیم وب‌هوک یا polling برای دریافت پیام‌ها

---

## 📦 مدیریت فایل و آپلود

### `get_upload_url(media_type)`
دریافت آدرس آپلود فایل برای انواع مختلف: File, Image, Voice, Music, Gif

### `upload_media_file(upload_url, name, path)`
آپلود فایل از مسیر محلی یا URL به Rubika و دریافت `file_id`

---

## 🔄 دریافت بروزرسانی‌ها

### `get_updates(offset_id=None, limit=None)`
دریافت بروزرسانی‌ها (برای polling)


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

# مستندات پروژه: تایمر پیام در ربات Rubika

این پروژه یک ربات بر پایه کتابخانه‌ی `rubka` است که به کاربر امکان می‌دهد با استفاده از کی‌پد، یک تایمر تنظیم کرده و پس از پایان تایمر، پیامی برای او ارسال شود. تمرکز اصلی این مستند، بر روی کلاس `Job` است که برای زمان‌بندی اجرای دستورات استفاده شده است.

## ساختار کلی پروژه
- استفاده از کتابخانه `rubka` برای ارتباط با Rubika Bot API
- تعریف یک کی‌پد با گزینه‌های تاخیر زمانی مختلف (۱۰ الی ۱۵۰ ثانیه)
- استفاده از کلاس `Job` برای مدیریت اجرای زمان‌بندی‌شده یک تابع
- نمایش شمارش معکوس با به‌روزرسانی مداوم پیام

---

## کلاس `Job` چیست؟
کلاس `Job` در فایل `rubka.jobs` تعریف شده و هدف آن اجرای یک تابع خاص پس از گذشت یک بازه زمانی مشخص است.

### نحوه استفاده:
```python
from rubka.jobs import Job

job = Job(delay_in_seconds, callback_function)
```

### پارامترها:
| پارامتر | نوع | توضیح |
|--------|-----|-------|
| `delay_in_seconds` | `int` | مدت زمانی که باید قبل از اجرای تابع منتظر بماند |
| `callback_function` | `function` | تابعی که بعد از پایان زمان باید اجرا شود |

### ویژگی‌ها:
- اجرای غیرهمزمان (با استفاده از Thread داخلی)
- مناسب برای سناریوهایی مانند تایمرها، یادآورها و اعلان‌های زمان‌بندی شده

---

## مثال از استفاده در پروژه:

```python
def delayed_send():
    if user_id not in active_jobs:
        return
    bot.send_message(
        message.chat_id,
        f"✅ کاربر {user_id} : زمان {seconds} ثانیه گذشت و دستور اجرا شد! ⏰"
    )
    active_jobs.pop(user_id, None)

job = Job(seconds, delayed_send)
active_jobs[user_id] = job
```

در این مثال، پس از انتخاب تاخیر زمانی توسط کاربر، یک شی از کلاس `Job` ساخته می‌شود که تابع `delayed_send` را پس از `seconds` ثانیه اجرا می‌کند.

---

## تابع `countdown_edit`
این تابع تایمر فعال را به صورت زنده باقیمانده زمان را به‌روزرسانی می‌کند:
```python
def countdown_edit(chat_id, message_id, duration_sec):
    # اجرای یک Thread برای به‌روزرسانی پیام در هر ثانیه
```

---
## نمونه کد ساخته شده
```python
from rubka import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from rubka.jobs import Job
from datetime import datetime, timedelta
import threading
import time

bot = Robot("token")

active_jobs = {}

def build_delay_keypad():
    delays = [10, 20, 30, 40, 50, 60, 75, 90, 120, 150]
    builder = ChatKeypadBuilder()
    buttons = []
    for sec in delays:
        buttons.append(builder.button(id=f"delay_{sec}", text=f"⏳ بعد از {sec} ثانیه"))
    buttons.append(builder.button(id="cancel", text="❌ انصراف"))
    
    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    keypad = ChatKeypadBuilder()
    for row in rows:
        keypad.row(*row)
    return keypad.build()

def countdown_edit(chat_id: str, message_id: str, duration_sec: int):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_sec)

    def run():
        while True:
            now = datetime.now()
            if now >= end_time:
                try:
                    bot.edit_message_text(chat_id, message_id, "⏰ زمان تمام شد!")
                except Exception as e:
                    print("خطا در ویرایش پیام:", e)
                break

            remaining = end_time - now
            text = (
                f"⏳ تایمر فعال است...\n"
                f"🕰 شروع: {start_time.strftime('%H:%M:%S')}\n"
                f"⏲ پایان: {end_time.strftime('%H:%M:%S')}\n"
                f"⌛ باقی‌مانده: {str(remaining).split('.')[0]}"
            )
            try:
                bot.edit_message_text(chat_id, message_id, text)
            except Exception as e:
                print("خطا در ویرایش پیام:", e)
            time.sleep(1)

    threading.Thread(target=run, daemon=True).start()

@bot.on_message(commands=["start"])
def start_handler(bot: Robot, message: Message):
    keypad = build_delay_keypad()
    message.reply_keypad(
        "سلام 👋\n"
        "یک زمان برای ارسال پیام انتخاب کنید:\n"
        "📅 تاریخ و ساعت فعلی: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        keypad
    )

@bot.on_callback()
def callback_delay(bot: Robot, message: Message):
    btn_id = message.aux_data.button_id
    user_id = message.sender_id
    
    if btn_id == "cancel":
        if user_id in active_jobs:
            active_jobs.pop(user_id)
            message.reply("❌ همه ارسال‌های زمان‌بندی شده لغو شدند.")
        else:
            message.reply("⚠️ شما هیچ ارسال زمان‌بندی شده‌ای ندارید.")
        return
    
    if not btn_id.startswith("delay_"):
        message.reply("❌ دکمه نامعتبر است!")
        return
    
    seconds = int(btn_id.split("_")[1])
    
    if user_id in active_jobs:
        active_jobs.pop(user_id)

    sent_msg = bot.send_message(
        message.chat_id,
        f"⏳ تایمر {seconds} ثانیه‌ای شروع شد...\n🕰 زمان شروع: {datetime.now().strftime('%H:%M:%S')}"
    )
    
    countdown_edit(message.chat_id, sent_msg['data']['message_id'], seconds)
    def delayed_send():
        if user_id not in active_jobs:
            return
        bot.send_message(
            message.chat_id,
            f"✅ کاربر {user_id} : زمان {seconds} ثانیه گذشت و دستور اجرا شد! ⏰"
        )
        active_jobs.pop(user_id, None)

    job = Job(seconds, delayed_send)
    active_jobs[user_id] = job

    message.reply(
        f"⏳ ثبت شد! پیام شما پس از {seconds} ثانیه ارسال خواهد شد.\n"
        f"🕰 زمان شروع ثبت شده: {datetime.now().strftime('%H:%M:%S')}"
    )
bot.run()
```

##مثال ساده تر
```python
from rubka import Robot
from rubka.context import Message
from rubka.jobs import Job
from datetime import datetime

bot = Robot("")

active_jobs = {}

@bot.on_message(commands=["timer"])
def timer_handler(bot: Robot, message: Message):
    user_id = message.sender_id
    chat_id = message.chat_id
    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        return message.reply("⚠️ لطفاً مدت زمان را به صورت صحیح وارد کنید. مثل: `/timer 30`", parse_mode="markdown")

    seconds = int(parts[1])
    if user_id in active_jobs:
        active_jobs.pop(user_id)

    message.reply(f"⏳ تایمر {seconds} ثانیه‌ای شروع شد!\n🕰 زمان شروع: {datetime.now().strftime('%H:%M:%S')}")

    def after_delay():
        if user_id not in active_jobs:
            return
        bot.send_message(chat_id, f"✅ تایمر {seconds} ثانیه‌ای تمام شد! ⏰")
        active_jobs.pop(user_id, None)

    job = Job(seconds, after_delay)
    active_jobs[user_id] = job

bot.run()

```

##نمونه کد ادیت تایم و کرون جاب با اینلاین کیبورد 

```python
from rubka import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from rubka.jobs import Job
from datetime import datetime, timedelta
import threading
import time

bot = Robot("token")
bot.edit_inline_keypad
active_jobs = {}

def build_delay_keypad():
    delays = [10, 20, 30, 40, 50, 60, 75, 90, 120, 150]
    builder = ChatKeypadBuilder()
    buttons = []
    for sec in delays:
        buttons.append(builder.button(id=f"delay_{sec}", text=f"⏳ بعد از {sec} ثانیه"))
    buttons.append(builder.button(id="cancel", text="❌ انصراف"))
    
    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    keypad = ChatKeypadBuilder()
    for row in rows:
        keypad.row(*row)
    return keypad.build()

def countdown_edit(chat_id: str, message_id: str, duration_sec: int):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_sec)

    def run():
        while True:
            now = datetime.now()
            if now >= end_time:
                try:
                    bot.edit_message_text(chat_id, message_id, "⏰ زمان تمام شد!")
                except Exception as e:
                    print("خطا در ویرایش پیام:", e)
                break

            remaining = end_time - now
            text = (
                f"⏳ تایمر فعال است...\n"
                f"🕰 شروع: {start_time.strftime('%H:%M:%S')}\n"
                f"⏲ پایان: {end_time.strftime('%H:%M:%S')}\n"
                f"⌛ باقی‌مانده: {str(remaining).split('.')[0]}"
            )
            try:
                bot.edit_message_text(chat_id, message_id, text)
            except Exception as e:
                print("خطا در ویرایش پیام:", e)
            time.sleep(1)

    threading.Thread(target=run, daemon=True).start()

@bot.on_message(commands=["start"])
def start_handler(bot: Robot, message: Message):
    keypad = build_delay_keypad()
    message.reply_keypad(
        "سلام 👋\n"
        "یک زمان برای ارسال پیام انتخاب کنید:\n"
        "📅 تاریخ و ساعت فعلی: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        keypad
    )

@bot.on_callback()
def callback_delay(bot: Robot, message: Message):
    btn_id = message.aux_data.button_id
    user_id = message.sender_id
    
    if btn_id == "cancel":
        if user_id in active_jobs:
            active_jobs.pop(user_id)
            message.reply("❌ همه ارسال‌های زمان‌بندی شده لغو شدند.")
        else:
            message.reply("⚠️ شما هیچ ارسال زمان‌بندی شده‌ای ندارید.")
        return
    if not btn_id.startswith("delay_"):
        message.reply("❌ دکمه نامعتبر است!")
        return
    seconds = int(btn_id.split("_")[1])
    if user_id in active_jobs:
        active_jobs.pop(user_id)
    sent_msg = bot.edit_inline_keypad(
        message.chat_id,
        f"⏳ تایمر {seconds} ثانیه‌ای شروع شد...\n🕰 زمان شروع: {datetime.now().strftime('%H:%M:%S')}"
    )
    print(sent_msg)
    countdown_edit(message.chat_id, sent_msg['data']['message_id'], seconds)
    def delayed_send():
        if user_id not in active_jobs:
            return
        
        bot.send_message(
            message.chat_id,
            f"✅ کاربر {user_id} : زمان {seconds} ثانیه گذشت و دستور اجرا شد! ⏰"
        )
        active_jobs.pop(user_id, None)

    job = Job(seconds, delayed_send)
    active_jobs[user_id] = job

    message.reply(
        f"⏳ ثبت شد! پیام شما پس از {seconds} ثانیه ارسال خواهد شد.\n"
        f"🕰 زمان شروع ثبت شده: {datetime.now().strftime('%H:%M:%S')}"
    )

bot.run()
```
# ✅ Force Join (اجبار به عضویت در کانال) — Rubka Bot

این مستند نحوه استفاده از قابلیت **اجبار به عضویت در یک کانال (Force Join)** در ربات‌های ساخته‌شده با کتابخانه Rubka را توضیح می‌دهد.

---

## 🎯 هدف

اطمینان از اینکه کاربر عضو یک کانال خاص است، قبل از ادامه تعامل با ربات. اگر عضو نبود، به او اطلاع داده شود یا لینک عضویت ارسال گردد.

---

## 📦 پیش‌نیازها

- نصب و راه‌اندازی کتابخانه `rubka`
- توکن معتبر ربات Rubika
- دسترسی به `channel_guid` (شناسه عددی کانال)
- ربات باید در کانال، **ادمین** باشد

---

## 💡 نحوه استفاده

### کد بهینه‌شده:

```python
from rubka import Robot
from rubka.context import Message

bot = Robot(token="your_token")
CHANNEL_GUID = "c0xABCDEF..."  # GUID کانال هدف

@bot.on_message()
def handle_force_join(bot: Robot, message: Message):
    name = bot.get_name(message.chat_id)

    if bot.check_join(CHANNEL_GUID, message.chat_id):
        message.reply(f"سلام {name} 👋\nشما عضو کانال هستید ✅")
    else:
        join_link = "https://rubika.ir/rubka_library"
        message.reply(
            f"سلام {name} 👋\nشما عضو کانال نیستید ❌\n\n"
            f"لطفاً ابتدا عضو کانال شوید سپس دوباره تلاش کنید:\n{join_link}"
        )

bot.run()
```

---

## 🔍 شرح متدها

| متد                                   | کاربرد                               |
| ------------------------------------- | ------------------------------------ |
| `check_join(channel_guid, user_guid)` | بررسی عضویت کاربر در کانال مشخص‌شده  |
| `get_name(user_guid)`                 | دریافت نام نمایشی کاربر از طریق GUID |
| `message.reply(text)`                 | پاسخ مستقیم به پیام دریافت‌شده       |

---

## 🔐 نکات مهم امنیتی

- ربات باید حتماً **ادمین کانال** باشد.
- در صورت عدم عضویت، بهتر است لینک دعوت به کانال نمایش داده شود.

##Mahdi Ahmadi
