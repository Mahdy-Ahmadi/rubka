from rubka import Robot
from rubka.keypad import ChatKeypadBuilder
from rubka.context import Message
import requests
import random
import time

bot = Robot("توکن")


license_keys = [
    "9abc08b313f37618ab50fe75e236ade7",
    "edcca599a45a45279a37dd485945168e",
    "698825483ce84f10813e9202996996ae",
    "99464dde6f9571772c9d59831112725e"
]


main_keypad = (
    ChatKeypadBuilder()
    .row(ChatKeypadBuilder().button("1", "🤖 هوش مصنوعی"))
    .row(ChatKeypadBuilder().button("2", "🎨 ساخت تصویر با متن"))
    .row(ChatKeypadBuilder().button("3", "🎎 تصویر انیمه"))
    .row(ChatKeypadBuilder().button("4", "📢 کانال"), ChatKeypadBuilder().button("5", "💬 پشتیبانی"))
    .row(ChatKeypadBuilder().button("6", "📘 راهنما"))
    .row(ChatKeypadBuilder().button("7", "🧠 دانستنی"), ChatKeypadBuilder().button("8", "😂 جوک"))
    .row(ChatKeypadBuilder().button("9", "📄 بیو"))
    .build()
)

def resp(api):
    return requests.get(api)

@bot.on_message()
def handle(bot, message: Message):
    text = message.text.strip()
    session = message.session
    if text == "/start":
        session.clear()
        message.reply_keypad("سلام به ربات خوش اومدی! یکی از گزینه‌های زیر رو انتخاب کن 👇", keypad=main_keypad)
        return

    if text == "📘 راهنما":
        message.reply(
            "📘 راهنما:\n"
            "- 🤖 هوش مصنوعی: ارسال سوال به چت‌جی‌پی‌تی\n"
            "- 🎨 ساخت تصویر: تبدیل متن به عکس\n"
            "- 🎎 تصویر انیمه: ساخت چهره انیمه تصادفی\n"
            "- 🧠 دانستنی: نمایش دانستنی تصادفی\n"
            "- 😂 جوک: جوک بامزه\n"
            "- 📄 بیو: بیوگرافی آماده برای پروفایل\n"
            "- 📢 کانال / 💬 پشتیبانی: ارتباط با ما"
        )
        return

    if text == "📄 بیو":
        sent = message.reply("⏳ در حال دریافت بیو...")
        try:
            bio = resp("https://api-free.ir/api/bio.php").text
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], f"📄 بیو آماده:\n{bio}")
        except:
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], "❌ خطا در دریافت بیو.")
        return

    if text == "😂 جوک":
        sent = message.reply("⏳ در حال دریافت جوک...")
        try:
            joke = resp("https://api-free.ir/api/jok.php").json().get("result")
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], f"😂 جوک:\n{joke}")
        except:
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], "❌ خطا در دریافت جوک.")
        return

    if text == "🧠 دانستنی":
        sent = message.reply("⏳ در حال دریافت دانستنی...")
        try:
            info = resp("https://api-free.ir/api/danes.php").text
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], f"🧠 دانستنی:\n{info}")
        except:
            bot.edit_message_text(message.chat_id, sent["data"]["message_id"], "❌ خطا در دریافت دانستنی.")
        return


    if text == "🤖 هوش مصنوعی":
        session["mode"] = "chatgpt"
        message.reply("🧠 سوال یا درخواستت رو بفرست:")
        return

    if text == "🎨 ساخت تصویر با متن":
        session["mode"] = "image_gen"
        message.reply("🖌️ لطفاً یک جمله یا کلمه بفرست:")
        return

    if text == "🎎 تصویر انیمه":
        sent = message.reply("⏳ لطفاً منتظر بمانید...")
        try:
            token = random.choice(license_keys)
            res = resp(f"https://api-free.ir/api2/enime.php?token={token}")
            result = res.json().get("result")
            final_text = f"🎎 تصویر ساخته‌شده:\n{result}" if result else "❌ خطا در دریافت تصویر."
        except:
            final_text = "❌ خطا در دریافت تصویر انیمه."
        bot.edit_message_text(message.chat_id, sent["data"]["message_id"], final_text)
        return

    if text == "📢 کانال":
        message.reply("📢 لینک کانال:\n@hakhaman_b2")
        return

    if text == "💬 پشتیبانی":
        message.reply("💬 ارتباط با پشتیبانی:\n@thevillain_tk")
        return

    # بررسی حالت session
    mode = session.get("mode")

    if mode == "chatgpt":
        sent = message.reply("⏳ لطفاً منتظر بمانید...")
        try:
            res = resp(f"https://api-free.ir/api/chat-gpt.php?text={text}")
            result = res.json().get("result") or res.json().get("Result")
            final_text = result if result else "❌ جوابی دریافت نشد."
        except:
            final_text = "❌ خطا در ارتباط با سرور."
        bot.edit_message_text(message.chat_id, sent["data"]["message_id"], final_text)
        return

    if mode == "image_gen":
        sent = message.reply("⏳ لطفاً منتظر بمانید...")
        try:
            res = resp(f"http://v3.api-free.ir/image/?text={text}")
            result = res.json().get("result")
            final_text = f"🖼️ تصویر ساخته‌شده:\n{result}" if result else "❌ تصویری دریافت نشد."
        except:
            final_text = "❌ خطا در ساخت تصویر."
        bot.edit_message_text(message.chat_id, sent["data"]["message_id"], final_text)
        return

    message.reply("❗ لطفاً ابتدا دستور /start را ارسال کنید.")

bot.run()
