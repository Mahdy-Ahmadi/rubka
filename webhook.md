# راهنمای کامل فعال‌سازی Webhook در ربات RubikaBot

## مرحله ۱: ساخت فایل PHP وب‌هوک

1. یک فایل متنی جدید بسازید و نام آن را مثلاً `webhook_logger.php` قرار دهید.  
2. کد زیر را داخل آن کپی و ذخیره کنید:

```php
<?php
$count = 20;
header("Content-Type: application/json");
$file_name = "message.json";
$file_path = __DIR__ . "/" . $file_name;
$protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? "https" : "http";
$host = $_SERVER['HTTP_HOST'];
$script_dir = rtrim(dirname($_SERVER['SCRIPT_NAME']), '/\');
$file_url = $protocol . "://" . $host . $script_dir . "/" . $file_name;
$input = file_get_contents("php://input");
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || empty($input)) {
    echo json_encode([
        "status" => "no data received",
        "url" => $file_url
    ], JSON_PRETTY_PRINT);
    exit;
}
$data = json_decode($input, true);
if ($data === null) {
    http_response_code(400);
    echo json_encode([
        "error" => "Invalid JSON",
        "url" => $file_url
    ], JSON_PRETTY_PRINT);
    exit;
}
$messages = [];
if (file_exists($file_path)) {
    $content = file_get_contents($file_path);
    $messages = json_decode($content, true);
    if (!is_array($messages)) {
        $messages = [];
    }
}
$messages[] = [
    "received_at" => date("Y-m-d H:i:s"),
    "data" => $data
];
while (count($messages) > $count) {
    array_shift($messages);
}
file_put_contents($file_path, json_encode($messages, JSON_PRETTY_PRINT));
echo json_encode([
    "status" => "ok",
    "received_at" => date("Y-m-d H:i:s"),
    "received_data" => $data,
    "url" => $file_url
], JSON_PRETTY_PRINT);
```

---

## مرحله ۲: آپلود فایل PHP روی هاست یا سرور

1. با استفاده از FTP، File Manager هاست، یا هر روش دیگر، فایل `webhook_logger.php` را در پوشه‌ای از وب‌سایت خود (مثلاً `public_html` یا `www`) آپلود کنید.  
2. مطمئن شوید که سرور شما از PHP پشتیبانی می‌کند و قابلیت اجرای فایل PHP را دارد.  
3. پس از آپلود، آدرس کامل فایل روی اینترنت چیزی شبیه به این خواهد بود:

```
https://yourdomain.com/path/to/webhook_logger.php
```

---

## مرحله ۳: وارد کردن آدرس وب‌هوک در کلاس Robot

در کد پایتون خود هنگام ساخت ربات، مقدار پارامتر `web_hook` را برابر با آدرس فایل PHP آپلودشده قرار دهید:

```python
from rubka import Robot

bot = Robot(
    token="YOUR_BOT_TOKEN",
    web_hook="https://yourdomain.com/path/to/webhook_logger.php"
)

bot.run()
```

---

## مرحله ۴: شروع به کار ربات

با اجرای کد پایتون بالا، ربات شما پیام‌ها را از طریق وب‌هوک (Push) دریافت می‌کند و به جای اینکه به صورت دوره‌ای پیام‌ها را بگیرد (Polling)، مستقیم پیام‌ها به ربات ارسال می‌شود.

---

## مرحله ۵: مشاهده پیام‌های دریافتی

در پوشه‌ای که فایل `webhook_logger.php` را آپلود کرده‌اید، فایلی به نام `message.json` ساخته می‌شود.  
برای دیدن پیام‌های ذخیره‌شده می‌توانید به آدرس زیر بروید:

```
https://yourdomain.com/path/to/message.json
```

---

## نکته

- این فایل فقط برای ذخیره موقت پیام‌ها جهت مشاهده و اشکال‌زدایی است.  
- بهتر است بعد از اطمینان از عملکرد وب‌هوک، این فایل را مدیریت یا پاک کنید.

---

اگر جای خاصی نیاز به توضیح بیشتر داشتی، بگو تا راهنمای دقیق‌تری بدم!

---

## نمونه کد کامل ارسال دکمه‌ها به صورت جداگانه و هندل کردن کلیک‌ها

```python
from rubka import Robot
from rubka.context import Message, InlineMessage
from rubka.button import InlineBuilder

bot = Robot(token="token", web_hook='https://...')

button_funcs = [
    lambda: InlineBuilder().row(InlineBuilder().button_simple("simple", "🔘 ساده")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_camera_image("camera_img", "📷 عکس با دوربین")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_camera_video("camera_vid", "🎥 ویدیو با دوربین")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_gallery_image("gallery_img", "🖼 عکس از گالری")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_gallery_video("gallery_vid", "🎞 ویدیو از گالری")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_audio("audio", "🎧 ارسال صوت")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_record_audio("rec_audio", "🎙 ضبط صوت")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_file("file", "📁 ارسال فایل")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_my_phone_number("my_phone", "📱 شماره من")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_ask_my_phone_number("ask_phone", "📞 دریافت شماره")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_my_location("my_loc", "📍 لوکیشن من")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_ask_location("ask_loc", "🌍 دریافت مکان")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_textbox("textbox", "📝 وارد کردن متن", "SingleLine", "String")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_number_picker("number_pick", "🔢 عدد", "1", "10")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_string_picker("string_pick", "📚 انتخاب متن", ["A", "B", "C"])).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_calendar("calendar", "📅 تقویم", "DatePersian")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_location("map", "🗺 نقشه", "Picker", "https://api-free.ir")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_barcode("barcode", "🔍 اسکن بارکد")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_payment("payment", "💰 پرداخت", 1000, "برای تست")).build(),
    lambda: InlineBuilder().row(InlineBuilder().button_link("link", "🔗 لینک", "https://rubika.ir/rubka_library")).build()
]

@bot.on_message(commands=["all"])
def send_buttons_separately(bot: Robot, message: Message):
    for index, btn_func in enumerate(button_funcs):
        try:
            inline_keypad = btn_func()
            message.reply_inline(f"🔘 دکمه {index+1}:", inline_keypad=inline_keypad)
        except Exception as e:
            message.reply(f"❌ خطا در ارسال دکمه {index+1}: {e}", is_rtl=True)

@bot.on_inline_query()
def handle_click(bot: Robot, message: InlineMessage):
    btn_id = message.aux_data.button_id
    print(message.raw_data)
    message.reply(f"✅ دکمه کلیک‌شده: \n\n{message.raw_data}")

bot.run()
```
