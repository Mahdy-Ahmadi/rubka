from rubka.asynco import Robot, Message, filters

ADMIN_ID = ['u0Ife3d0c3351b1e2e312a58dc9c7760']#ادمین های گروه (sender_id)

bot = Robot("", api_endpoint="messenger")

bot.start_save_message()

rules_config,rules_fa = {
    "active": True,
    "link": True,
    "mention": True,
    "hashtag": False,
    "emoji": False,
    "only_emoji": False,
    "number": False,
    "command": False,
    "metadata": True,
    "bold": False,
    "italic": False,
    "underline": False,
    "strike": False,
    "quote": False,
    "spoiler": False,
    "code": False,
    "mono": False,
    "photo": False,
    "video": False,
    "audio": False,
    "voice": False,
    "music": False,
    "document": False,
    "archive": False,
    "executable": False,
    "font": False,
    "sticker": False,
    "forward": True,
    "contact": False,
    "location": False,
    "live_location": False,
    "poll": False,
    "anti_flood": True
},{
    "active": "فعال",
    "link": "لینک",
    "mention": "منشن",
    "hashtag": "هشتگ",
    "emoji": "ایموجی",
    "only_emoji": "فقط ایموجی",
    "number": "عدد",
    "command": "دستور",
    "metadata": "متادیتا",
    "bold": "متن بولد",
    "italic": "متن ایتالیک",
    "underline": "زیرخط",
    "strike": "خط خورده",
    "quote": "کوت",
    "spoiler": "اسپویلر",
    "code": "کد",
    "mono": "مونواسپیس",
    "photo": "عکس",
    "video": "ویدیو",
    "audio": "صوت",
    "voice": "ویس",
    "music": "موزیک",
    "document": "سند / فایل",
    "archive": "فایل فشرده",
    "executable": "فایل اجرایی",
    "font": "فونت",
    "sticker": "استیکر",
    "forward": "فوروارد",
    "contact": "شماره تماس",
    "location": "لوکیشن",
    "live_location": "لوکیشن زنده",
    "poll": "نظرسنجی",
    "anti_flood": "کد هنگی"
}

def check_rules(message: Message):
    if not rules_config["active"]:return []
    violations = []
    if rules_config["link"] and message.has_link:violations.append("لینک")
    if rules_config.get("anti_flood") and message.text and message.text.count(".") >= 40:violations.append("کد هنگی")
    if rules_config["mention"] and message.is_mention:violations.append("منشن")
    if rules_config["hashtag"] and message.is_hashtag:violations.append("هشتگ")
    if rules_config["emoji"] and message.is_emoji:violations.append("ایموجی")
    if rules_config["only_emoji"] and message.is_pure_emoji:violations.append("فقط ایموجی")
    if rules_config["number"] and message.is_number:violations.append("عدد")
    if rules_config["command"] and message.is_command:violations.append("استفاده از دستور")
    if rules_config["metadata"] and message.has_metadata:violations.append("متادیتا")
    if rules_config["bold"] and message.is_bold:violations.append("متن بولد")
    if rules_config["italic"] and message.is_italic:violations.append("متن ایتالیک")
    if rules_config["underline"] and message.is_underline:violations.append("زیرخط")
    if rules_config["strike"] and message.is_strike:violations.append("خط خورده")
    if rules_config["quote"] and message.is_quote:violations.append("کوت")
    if rules_config["spoiler"] and message.is_spoiler:violations.append("اسپویلر")
    if rules_config["code"] and message.is_pre:violations.append("کد")
    if rules_config["mono"] and message.is_mono:violations.append("مونواسپیس")
    if rules_config["photo"] and message.is_photo:violations.append("عکس")
    if rules_config["video"] and message.is_video:violations.append("ویدیو")
    if rules_config["audio"] and message.is_audio:violations.append("صوت")
    if rules_config["voice"] and message.is_voice:violations.append("ویس")
    if rules_config["music"] and message.is_music:violations.append("موزیک")
    if rules_config["document"] and message.is_document:violations.append("سند / فایل")
    if rules_config["archive"] and message.is_archive:violations.append("فایل فشرده")
    if rules_config["executable"] and message.is_executable:violations.append("فایل اجرایی")
    if rules_config["font"] and message.is_font:violations.append("فونت")
    if rules_config["sticker"] and message.sticker:violations.append("استیکر")
    if rules_config["forward"] and message.is_forwarded:violations.append("فوروارد")
    if rules_config["contact"] and message.is_contact:violations.append("شماره تماس")
    if rules_config["location"] and message.is_location:violations.append("لوکیشن")
    if rules_config["live_location"] and message.is_live_location:violations.append("لوکیشن زنده")
    if rules_config["poll"] and message.is_poll:violations.append("نظرسنجی")
    return violations

@bot.on_message()
async def user_message(bot, message: Message):
    if message.sender_id not in ADMIN_ID:
        violations = check_rules(message)
        if violations:
            texts = " و ".join(violations)
            await message.reply(
                f"⛔ **اخطار**\n"
                f">درود [کاربر]({message.sender_id}) عزیز\n"
                f"📌 دلیل : {texts}\n",
                30
            )
            await message.delete()

@bot.on_message(filters.senders_id(ADMIN_ID))
async def admin_message(bot: Robot, message: Message):
    text = message.text.strip()
    await message.delete()
    reply_id = message.reply_to_message_id
    await message.copy_message(to_chat_id=message.chat_id, message_id=reply_id)
    if text == "وضعیت":
        state = "\n".join([f">🔹 {rules_fa[k]} : {'روشن' if v else 'خاموش'}" for k, v in rules_config.items()])
        return await bot.send_message(chat_id=message.chat_id, text=state)
    if text == "خاموش همه":
        for k in rules_config:rules_config[k] = False
        return await bot.send_message(chat_id=message.chat_id, text=">🔕 همه قوانین خاموش شدند.")
    if text == "روشن همه":
        for k in rules_config:rules_config[k] = True
        return await bot.send_message(chat_id=message.chat_id, text=">🔔 همه قوانین روشن شدند.")
    for k in rules_config:
        if text == f"قفل {rules_fa[k]}" or text == f"{rules_fa[k]}":
            rules_config[k] = not rules_config[k]
            new = "روشن" if rules_config[k] else "خاموش"
            return await bot.send_message(chat_id=message.chat_id, text=f"✔️ وضعیت **{rules_fa[k]}** تغییر کرد.\n> وضعیت جدید: **{new}**")
    
    if text in ["get", "اطلاعات", "info"] and reply_id:
        info = await bot.get_message(message.chat_id, reply_id)
        return await bot.send_message(chat_id=message.chat_id, text=f"**اطلاعات پیام:**\n>{info}", reply_to_message_id=reply_id)

@bot.on_message(filters.text_equals("راهنما"))
async def user_message2(bot, message: Message):
    await message.reply(f"[سورس این ربات جهت استفاده عمومی به صورت پابلیک قرار دارد لطفا جهت دیدن کلیک کنید](https://github.com/Mahdy-Ahmadi/rubka/blob/main/test-bots/test-get_message.py)")

bot.run(sleep_time=0)
