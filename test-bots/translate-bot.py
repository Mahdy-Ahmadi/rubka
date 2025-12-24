from rubka.asynco import Robot, Message, ChatKeypadBuilder

bot = Robot("token")

languages = [
    ('fa', 'فارسی'),('ku', 'کردی رسمی'),('az', 'آذری'),('tk', 'ترکمنی'),('hr', 'هرزگان'),('khb', 'خوزی'),('ps', 'پشتو'),('ckb', 'کوردی کرمانشاه'),
    ('en', 'انگلیسی'),('fa', 'فارسی'),('es', 'اسپانیایی'),('de', 'آلمانی'),('fr', 'فرانسوی'),('it', 'ایتالیایی'),('pt', 'پرتغالی'),('ru', 'روسی'),
    ('ar', 'عربی'),('zh', 'چینی'),('ja', 'ژاپنی'),('ko', 'کره‌ای'),('hi', 'هندی'),('tr', 'ترکی'),('pl', 'لهستانی'),('nl', 'هلندی'),('sv', 'سوئدی'),
    ('da', 'دانمارکی'),('no', 'نروژی'),('fi', 'فنلاندی'),('cs', 'چکی'),('sk', 'اسلواکی'),('ro', 'رومانیایی'),('bg', 'بلغاری'),('hu', 'مجاری'),
    
]


def build_language_keypad():
    keypad = ChatKeypadBuilder()
    row_buttons = []
    for idx, (lang_code, lang_name) in enumerate(languages):
        row_buttons.append(ChatKeypadBuilder().button(id=lang_code, text=lang_name))
        if (idx + 1) % 4 == 0 or idx == len(languages) - 1:
            keypad = keypad.row(*row_buttons)
            row_buttons = []

    return keypad.build()

language_keypad = build_language_keypad()

user_language = {}

@bot.on_message(commands=['start'])
async def start(bot: Robot, message: Message):
    await message.reply(
        "سلام! لطفا زبان مورد نظر خود را از دکمه‌های زیر انتخاب کنید:",
        chat_keypad=language_keypad,
        chat_keypad_type="New"
    )

@bot.on_callback()
async def handle_language_selection(bot: Robot, message: Message):
    language_code = message.aux_data.button_id
    if language_code in dict(languages):
        user_language[message.sender_id] = language_code
        await message.answer(f"زبان به {dict(languages).get(language_code)} تغییر کرد. حالا می‌توانید متنی ارسال کنید تا ترجمه شود.")
    else:
        await message.answer("زبان انتخابی معتبر نیست.")

@bot.on_message()
async def handle_translation(bot: Robot, message: Message):
    if message.sender_id in user_language:
        target_language = user_language[message.sender_id]
        try:translated_text = await bot.translate_message(message.text, target_language)
        except Exception as e:await message.reply(f"خطایی رخ داد !\n>زبان پشتیبانی نمیشود...")
        await message.reply(f"{translated_text}")
    else:await message.reply("لطفا ابتدا زبان خود را از منوی بالا انتخاب کنید.")

bot.run()
