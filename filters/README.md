# Rubka Filters Documentation

این داکیومنت برای معرفی کامل فیلترهای کتابخانه Rubka نوشته شده است. می‌توانید از این فیلترها برای دسته‌بندی و مدیریت پیام‌ها در ربات‌های خود استفاده کنید.

---

## 1. فیلترهای پایه (Basic Filters)

این فیلترها برای شناسایی نوع پیام و مشخصات کلی چت استفاده می‌شوند.

*   `is_text` : **بررسی می‌کند که آیا پیام از نوع متنی است.**
    ```python
    @bot.on_message(filters.is_text)
    async def handle_text_message(bot, msg: Message):
        await msg.reply("این یک پیام متنی است.")
    ```

*   `is_file` : **بررسی می‌کند که آیا پیام حاوی هر نوع فایلی است.**
    ```python
    @bot.on_message(filters.is_file)
    async def handle_file_message(bot, msg: Message):
        await msg.reply("این پیام حاوی یک فایل است.")
    ```

*   `is_sticker` : **بررسی می‌کند که آیا پیام حاوی استیکر است.**
    ```python
    @bot.on_message(filters.is_sticker)
    async def handle_sticker_message(bot, msg: Message):
        await msg.reply("شما یک استیکر ارسال کردید!")
    ```

*   `is_contact` : **بررسی می‌کند که آیا پیام حاوی اطلاعات تماس (مخاطب) است.**
    ```python
    @bot.on_message(filters.is_contact)
    async def handle_contact_message(bot, msg: Message):
        await msg.reply("اطلاعات تماس دریافت شد.")
    ```

*   `is_poll` : **بررسی می‌کند که آیا پیام حاوی نظرسنجی است.**
    ```python
    @bot.on_message(filters.is_poll)
    async def handle_poll_message(bot, msg: Message):
        await msg.reply("یک نظرسنجی جدید ایجاد شده است.")
    ```

*   `is_location` : **بررسی می‌کند که آیا پیام حاوی موقعیت مکانی ثابت است.**
    ```python
    @bot.on_message(filters.is_location)
    async def handle_location_message(bot, msg: Message):
        await msg.reply("موقعیت مکانی شما دریافت شد.")
    ```

*   `is_live_location` : **بررسی می‌کند که آیا پیام حاوی موقعیت مکانی زنده (Live Location) است.**
    ```python
    @bot.on_message(filters.is_live_location)
    async def handle_live_location_message(bot, msg: Message):
        await msg.reply("موقعیت مکانی زنده شما را دریافت کردیم.")
    ```

*   `has_any_media` : **بررسی می‌کند که آیا پیام حاوی هر نوع رسانه‌ای (عکس، ویدیو، صدا، فایل و...) است.**
    ```python
    @bot.on_message(filters.has_any_media)
    async def handle_any_media(bot, msg: Message):
        await msg.reply("پیام شما حاوی رسانه است.")
    ```

*   `has_media` : **بررسی می‌کند که آیا پیام حاوی مدیا (عکس، ویدیو، صدا) است.**
    ```python
    @bot.on_message(filters.has_media)
    async def handle_media(bot, msg: Message):
        await msg.reply("این پیام حاوی مدیا است (عکس، ویدیو یا صدا).")
    ```

*   `is_command` : **بررسی می‌کند که آیا پیام یک دستور (Command) با فرمت `/command` است.**
    ```python
    @bot.on_message(filters.is_command)
    async def handle_command(bot, msg: Message):
        await msg.reply(f"دستور شما: {msg.text}")
    ```

*   `is_user` : **بررسی می‌کند که آیا فرستنده پیام یک کاربر (Bot) است.**
    ```python
    @bot.on_message(filters.is_user)
    async def handle_user_message(bot, msg: Message):
        await msg.reply("شما یک کاربر عادی هستید.")
    ```

*   `is_private` : **بررسی می‌کند که آیا چت از نوع خصوصی (Private Chat) است.**
    ```python
    @bot.on_message(filters.is_private)
    async def handle_private_chat(bot, msg: Message):
        await msg.reply("این پیام در یک چت خصوصی دریافت شد.")
    ```

*   `is_group` : **بررسی می‌کند که آیا چت از نوع گروه (Group) است.**
    ```python
    @bot.on_message(filters.is_group)
    async def handle_group_chat(bot, msg: Message):
        await msg.reply("این پیام در یک گروه دریافت شد.")
    ```

*   `is_channel` : **بررسی می‌کند که آیا چت از نوع کانال (Channel) است.**
    ```python
    @bot.on_message(filters.is_channel)
    async def handle_channel_message(bot, msg: Message):
        await msg.reply("این پیام از یک کانال دریافت شد.")
    ```

*   `is_reply` : **بررسی می‌کند که آیا پیام یک پاسخ (Reply) به پیام دیگری است.**
    ```python
    @bot.on_message(filters.is_reply)
    async def handle_reply_message(bot, msg: Message):
        await msg.reply("شما به پیام قبلی پاسخ دادید.")
    ```

*   `is_forwarded` : **بررسی می‌کند که آیا پیام فوروارد شده است.**
    ```python
    @bot.on_message(filters.is_forwarded)
    async def handle_forwarded_message(bot, msg: Message):
        await msg.reply("این پیام فوروارد شده است.")
    ```

*   `is_edited` : **بررسی می‌کند که آیا پیام ویرایش شده است.**
    ```python
    @bot.on_message(filters.is_edited)
    async def handle_edited_message(bot, msg: Message):
        await msg.reply("این پیام ویرایش شده است.")
    ```

---

## 2. فیلترهای متن (Text Filters)

این فیلترها برای بررسی محتوای متنی پیام استفاده می‌شوند.

*   `text(keyword: str)` : **بررسی می‌کند که آیا متن پیام حاوی کلمه کلیدی مشخص شده است.**
    ```python
    @bot.on_message(filters.text("سلام"))
    async def handle_hello(bot, msg: Message):
        await msg.reply("سلام به شما!")
    ```

*   `text_length(min_len: int, max_len: int)` : **بررسی می‌کند که طول متن پیام در محدوده مشخص شده (شامل حد بالا و پایین) باشد.**
    ```python
    @bot.on_message(filters.text_length(min_len=10, max_len=50))
    async def handle_medium_text(bot, msg: Message):
        await msg.reply("طول پیام شما بین 10 تا 50 کاراکتر است.")
    ```

*   `text_regex(pattern: str)` : **بررسی می‌کند که آیا متن پیام با الگوی regex مشخص شده مطابقت دارد.**
    ```python
    @bot.on_message(filters.text_regex(r"^\/start"))
    async def handle_start_command_regex(bot, msg: Message):
        await msg.reply("شما از دستور start استفاده کردید (با regex).")

    @bot.on_message(filters.text_regex(r"\d{10}"))
    async def handle_phone_number_regex(bot, msg: Message):
        await msg.reply("پیامی حاوی یک شماره تلفن 10 رقمی دریافت شد.")
    ```

*   `text_startswith(prefix: str)` : **بررسی می‌کند که آیا متن پیام با پیشوند مشخص شده شروع می‌شود.**
    ```python
    @bot.on_message(filters.text_startswith("پشتیبانی:"))
    async def handle_support_request(bot, msg: Message):
        await msg.reply("درخواست پشتیبانی دریافت شد.")
    ```

*   `text_endswith(suffix: str)` : **بررسی می‌کند که آیا متن پیام با پسوند مشخص شده پایان می‌یابد.**
    ```python
    @bot.on_message(filters.text_endswith("؟"))
    async def handle_question(bot, msg: Message):
        await msg.reply("شما سوال پرسیدید!")
    ```

*   `text_upper()` : **بررسی می‌کند که آیا کل متن پیام با حروف بزرگ (Capital Letters) نوشته شده است.**
    ```python
    @bot.on_message(filters.text_upper())
    async def handle_all_caps(bot, msg: Message):
        await msg.reply("لطفاً با حروف بزرگ پیام ندهید.")
    ```

*   `text_lower()` : **بررسی می‌کند که آیا کل متن پیام با حروف کوچک (Lowercase Letters) نوشته شده است.**
    ```python
    @bot.on_message(filters.text_lower())
    async def handle_all_lowercase(bot, msg: Message):
        await msg.reply("همه حروف پیام شما کوچک بود.")
    ```

*   `text_digit()` : **بررسی می‌کند که آیا کل متن پیام فقط شامل ارقام (اعداد) است.**
    ```python
    @bot.on_message(filters.text_digit())
    async def handle_only_digits(bot, msg: Message):
        await msg.reply("فقط عدد دریافت شد.")
    ```

*   `text_word_count(min_words: int, max_words: int)` : **بررسی می‌کند که تعداد کلمات در متن پیام در محدوده مشخص شده باشد.**
    ```python
    @bot.on_message(filters.text_word_count(min_words=5, max_words=15))
    async def handle_medium_word_count(bot, msg: Message):
        await msg.reply("پیام شما بین 5 تا 15 کلمه دارد.")
    ```

*   `text_contains_any(keywords: list)` : **بررسی می‌کند که متن پیام حداقل شامل یکی از کلمات موجود در لیست باشد.**
    ```python
    @bot.on_message(filters.text_contains_any(["خرید", "فروش", "قیمت"]))
    async def handle_shopping_keywords(bot, msg: Message):
        await msg.reply("به نظر می‌رسد موضوع بحث شما خرید یا فروش است.")
    ```

*   `text_equals(value: str)` : **بررسی می‌کند که متن پیام دقیقاً برابر با مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.text_equals("دستور توقف"))
    async def handle_stop_command(bot, msg: Message):
        await msg.reply("دستور توقف دریافت شد.")
    ```

*   `text_not_equals(value: str)` : **بررسی می‌کند که متن پیام دقیقاً برابر با مقدار مشخص شده نباشد.**
    ```python
    @bot.on_message(filters.text_not_equals("هیچ"))
    async def handle_not_nothing(bot, msg: Message):
        await msg.reply("پیام شما 'هیچ' نبود.")
    ```

---

## 3. فیلترهای فایل (File Filters)

این فیلترها برای بررسی مشخصات فایل‌های ارسال شده در پیام استفاده می‌شوند.

*   `file_size_gt(size)` : **بررسی می‌کند که اندازه فایل (بر حسب بایت) بیشتر از مقدار مشخص شده باشد.**
    ```python
    # 1MB = 1024 * 1024 بایت
    @bot.on_message(filters.file_size_gt(1024 * 1024))
    async def handle_large_files(bot, msg: Message):
        await msg.reply("فایل ارسالی بزرگتر از 1MB است.")
    ```

*   `file_size_lt(size)` : **بررسی می‌کند که اندازه فایل (بر حسب بایت) کمتر از مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.file_size_lt(100 * 1024)) # 100KB
    async def handle_small_files(bot, msg: Message):
        await msg.reply("فایل ارسالی کوچکتر از 100KB است.")
    ```

*   `file_name_contains(substring)` : **بررسی می‌کند که نام فایل حاوی رشته متنی مشخص شده باشد.**
    ```python
    @bot.on_message(filters.file_name_contains("report"))
    async def handle_report_file(bot, msg: Message):
        await msg.reply("فایل گزارش دریافت شد.")
    ```

*   `file_extension(ext: str)` : **بررسی می‌کند که پسوند فایل با پسوند مشخص شده مطابقت داشته باشد (با نقطه شروع شود، مثلاً `.jpg`).**
    ```python
    @bot.on_message(filters.file_extension(".pdf"))
    async def handle_pdf_files(bot, msg: Message):
        await msg.reply("یک فایل PDF ارسال شد.")

    @bot.on_message(filters.file_extension(".mp3"))
    async def handle_mp3_files(bot, msg: Message):
        await msg.reply("یک فایل صوتی MP3 دریافت شد.")
    ```

*   `file_id_is(file_id: str)` : **بررسی می‌کند که شناسه فایل (File ID) با شناسه مشخص شده مطابقت داشته باشد.**
    ```python
    # فرض کنید file_id_of_your_sticker یک file_id استیکر خاص است
    @bot.on_message(filters.file_id_is("file_id_of_your_sticker"))
    async def handle_specific_sticker(bot, msg: Message):
        await msg.reply("این استیکر خاص شماست!")
    ```

---

## 4. فیلترهای گروه و کانال (Chat Filters)

این فیلترها برای بررسی مشخصات چت (گروه، کانال، سوپرگروه) استفاده می‌شوند.

*   `chat_title_contains(keyword: str)` : **بررسی می‌کند که عنوان چت (Title) حاوی کلمه کلیدی مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_title_contains("رسمی"))
    async def handle_official_chat(bot, msg: Message):
        await msg.reply("پیام در گروه یا کانال رسمی دریافت شد.")
    ```

*   `chat_title_equals(value: str)` : **بررسی می‌کند که عنوان چت دقیقاً برابر با مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_title_equals("گروه آزمایشی"))
    async def handle_test_group(bot, msg: Message):
        await msg.reply("سلام در گروه آزمایشی!")
    ```

*   `chat_title_regex(pattern: str)` : **بررسی می‌کند که عنوان چت با الگوی regex مشخص شده مطابقت داشته باشد.**
    ```python
    @bot.on_message(filters.chat_title_regex(r"^_private_.*"))
    async def handle_private_chats_by_title(bot, msg: Message):
        await msg.reply("پیام از یک چت خصوصی با الگوی عنوان خاص دریافت شد.")
    ```

*   `chat_id_is(cid: int)` : **بررسی می‌کند که شناسه چت (Chat ID) با شناسه مشخص شده مطابقت داشته باشد.**
    ```python
    # فرض کنید CHAT_ID_SPECIFIC یک ID چت است
    @bot.on_message(filters.chat_id_is(CHAT_ID_SPECIFIC))
    async def handle_specific_chat_id(bot, msg: Message):
        await msg.reply("این پیام از چت مورد نظر ما است.")
    ```

*   `chat_member_count(min_count: int, max_count: int)` : **بررسی می‌کند که تعداد اعضای چت در محدوده مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_member_count(min_count=100, max_count=500))
    async def handle_medium_sized_group(bot, msg: Message):
        await msg.reply("این گروه بین 100 تا 500 عضو دارد.")
    ```

*   `chat_type_is(chat_type: str)` : **بررسی می‌کند که نوع چت با مقدار مشخص شده مطابقت داشته باشد (مقادیر ممکن: 'group', 'supergroup', 'channel').**
    ```python
    @bot.on_message(filters.chat_type_is('supergroup'))
    async def handle_supergroups(bot, msg: Message):
        await msg.reply("پیام از یک سوپرگروه دریافت شد.")
    ```

*   `chat_username_contains(keyword: str)` : **بررسی می‌کند که یوزرنیم چت (اگر وجود داشته باشد) حاوی کلمه کلیدی مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_username_contains("bot"))
    async def handle_bot_username_chat(bot, msg: Message):
        await msg.reply("پیام از چتی با یوزرنیم حاوی 'bot' دریافت شد.")
    ```

*   `chat_username_equals(value: str)` : **بررسی می‌کند که یوزرنیم چت (اگر وجود داشته باشد) دقیقاً برابر با مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_username_equals("my_channel_name"))
    async def handle_specific_channel_username(bot, msg: Message):
        await msg.reply("پیام از کانال با یوزرنیم دقیق 'my_channel_name' دریافت شد.")
    ```

*   `chat_has_link()` : **بررسی می‌کند که چت مورد نظر دارای لینک عمومی (Public Link) باشد.**
    ```python
    @bot.on_message(filters.chat_has_link())
    async def handle_chat_with_link(bot, msg: Message):
        await msg.reply("این چت دارای لینک عمومی است.")
    ```

*   `chat_is_private()` : **بررسی می‌کند که چت از نوع خصوصی نباشد (یعنی گروه یا کانال باشد).**
    ```python
    @bot.on_message(filters.chat_is_private())
    async def handle_non_private_chats(bot, msg: Message):
        await msg.reply("این پیام در یک گروه یا کانال دریافت شده است.")
    ```

*   `chat_member_count_gt(count: int)` : **بررسی می‌کند که تعداد اعضای چت بیشتر از مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_member_count_gt(1000))
    async def handle_large_groups(bot, msg: Message):
        await msg.reply("این گروه بیش از 1000 عضو دارد.")
    ```

*   `chat_member_count_lt(count: int)` : **بررسی می‌کند که تعداد اعضای چت کمتر از مقدار مشخص شده باشد.**
    ```python
    @bot.on_message(filters.chat_member_count_lt(50))
    async def handle_small_groups(bot, msg: Message):
        await msg.reply("این گروه کمتر از 50 عضو دارد.")
    ```

*   `chat_has_username()` : **بررسی می‌کند که چت مورد نظر دارای یوزرنیم باشد.**
    ```python
    @bot.on_message(filters.chat_has_username())
    async def handle_chats_with_username(bot, msg: Message):
        await msg.reply("این چت دارای یوزرنیم است.")
    ```

*   `chat_type_in(types: list)` : **بررسی می‌کند که نوع چت در لیستی از انواع مشخص شده باشد (مثلاً `['group', 'supergroup']`).**
    ```python
    @bot.on_message(filters.chat_type_in(['group', 'supergroup']))
    async def handle_any_group_type(bot, msg: Message):
        await msg.reply("پیام از یک گروه یا سوپرگروه دریافت شد.")
    ```

---

## 5. فیلترهای ترکیبی و کمکی (Composite and Helper Filters)

این فیلترها برای ترکیب فیلترهای دیگر و ایجاد منطق پیچیده‌تر استفاده می‌شوند.

*   `and_(*filters)` : **این فیلتر زمانی درست است که تمام فیلترهای ورودی آن درست باشند.**
    ```python
    @bot.on_message(filters.and_(filters.is_group, filters.text_contains_any(["سلام", "درود"])))
    async def handle_greeting_in_group(bot, msg: Message):
        await msg.reply("سلام! خوش آمدید به گروه.")
    ```

*   `or_(*filters)` : **این فیلتر زمانی درست است که حداقل یکی از فیلترهای ورودی آن درست باشد.**
    ```python
    @bot.on_message(filters.or_(filters.is_sticker, filters.file_extension(".jpg")))
    async def handle_sticker_or_photo(bot, msg: Message):
        await msg.reply("شما استیکر یا عکس ارسال کردید.")
    ```

*   `not_(filter_)` : **این فیلتر زمانی درست است که فیلتر ورودی آن نادرست باشد.**
    ```python
    @bot.on_message(filters.not_(filters.is_private))
    async def handle_non_private_messages(bot, msg: Message):
        await msg.reply("پیام در یک چت غیرخصوصی دریافت شد.")
    ```

*   `custom(name: str)` : **برای استفاده از فیلترهای سفارشی که قبلاً تعریف کرده‌اید.**
    ```python
    # فرض کنید یک فیلتر سفارشی به نام 'is_admin' قبلاً تعریف شده است
    # @bot.register_filter('is_admin', lambda _, msg: msg.sender_id in ADMIN_IDS)

    @bot.on_message(filters.custom('is_admin'))
    async def handle_admin_message(bot, msg: Message):
        await msg.reply("پیام از طرف ادمین دریافت شد.")
    ```

*   `get_custom(name: str)` : **برای دریافت یک فیلتر سفارشی تعریف شده.**
    ```python
    admin_filter = filters.get_custom('is_admin')
    @bot.on_message(filters.is_group & admin_filter)
    async def handle_admin_in_group(bot, msg: Message):
        await msg.reply("ادمین در گروه پیام داد.")
    ```

---

## راه‌اندازی ربات (Robot Setup)

در اینجا نمونه‌ای از نحوه راه‌اندازی ربات Rubka و استفاده از فیلترها آورده شده است.

```python
import asyncio
from rubka.asynco import Robot, filters
from rubka.context import Message

# توکن ربات خود را اینجا قرار دهید
BOT_TOKEN = "YOUR_BOT_TOKEN" # مثال: "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg hijklm"

# نمونه‌ای از کلاس Robot
bot = Robot(BOT_TOKEN)

# فیلتری برای خوش‌آمدگویی به کاربران جدید در گروه‌ها
@bot.on_message(filters.is_group & filters.text_startswith("/start"))
async def welcome_new_member(bot, msg: Message):
    await msg.reply("خوش آمدید! این گروه یک گروه آزمایشی است.")

# فیلتری برای پاسخ به پیام‌های متنی در چت‌های خصوصی
@bot.on_message(filters.is_private & filters.is_text)
async def handle_private_text(bot, msg: Message):
    await msg.reply(f"پیام شما دریافت شد: '{msg.text}'")

# فیلتری برای مدیریت پیام‌های حاوی عکس در گروه‌ها
@bot.on_message(filters.is_group & filters.file_extension(".jpg"))
async def handle_group_jpg(bot, msg: Message):
    await msg.reply("یک عکس JPG در گروه ارسال شد.")

# فیلتر ترکیبی: پیام از گروه و حاوی کلمه "کمک"
@bot.on_message(filters.and_(filters.is_group, filters.text("کمک")))
async def help_in_group(bot, msg: Message):
    await msg.reply("چطور می‌توانم کمک کنم؟")

# فیلتر ترکیبی: پیام از کاربر یا گروه، و نه فوروارد شده
@bot.on_message(filters.or_(filters.is_user, filters.is_group) & filters.not_(filters.is_forwarded))
async def handle_original_messages(bot, msg: Message):
    await msg.reply("پیام اصلی شما دریافت شد.")

# فیلتری برای دریافت فایل‌های PDF از هر نوع چتی
@bot.on_message(filters.is_file & filters.file_extension(".pdf"))
async def handle_all_pdf_files(bot, msg: Message):
    await msg.reply("یک فایل PDF دریافت شد.")

# فیلتری برای دریافت پیام‌های متنی که دقیقاً "سلام" هستند
@bot.on_message(filters.text_equals("سلام"))
async def handle_exact_hello(bot, msg: Message):
    await msg.reply("سلام! دقیقا 'سلام' را تایپ کردید.")

# فیلتری برای گروه‌هایی که نامشان حاوی "مهم" است
@bot.on_message(filters.is_group & filters.chat_title_contains("مهم"))
async def handle_important_group(bot, msg: Message):
    await msg.reply("پیام از یک گروه مهم دریافت شد.")

# فیلتر ترکیبی: پیام از گروه یا سوپرگروه
@bot.on_message(filters.chat_type_in(['group', 'supergroup']))
async def handle_any_group_type(bot, msg: Message):
    await msg.reply(f"این پیام از یک {msg.chat.type} دریافت شد.")

# اجرای ربات
if __name__ == "__main__":
    asyncio.run(bot.run())
