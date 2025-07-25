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
