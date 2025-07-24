import threading
import time
from rubka import Robot
from rubka.keypad import ChatKeypadBuilder
from rubka.context import Message

bot = Robot("1")

main_keypad = (
    ChatKeypadBuilder()
    .row(
        ChatKeypadBuilder().button("bird", "پرنده 🐦"),
        ChatKeypadBuilder().button("heart", "قلب ❤️"),
        ChatKeypadBuilder().button("flower", "گل 🌸")
    )
    .row(
        ChatKeypadBuilder().button("walk", "پیاده‌روی 🚶"),
        ChatKeypadBuilder().button("run", "دویدن 🏃"),
        ChatKeypadBuilder().button("car", "ماشین 🚗")
    )
    .row(
        ChatKeypadBuilder().button("cat", "گربه 🐱"),
        ChatKeypadBuilder().button("dog", "سگ 🐶"),
        ChatKeypadBuilder().button("fish", "ماهی 🐟")
    )
    .row(
        ChatKeypadBuilder().button("rocket", "موشک 🚀"),
        ChatKeypadBuilder().button("dance", "رقص 💃"),
        ChatKeypadBuilder().button("clap", "دست زدن 👏")
    )
    .row(
        ChatKeypadBuilder().button("sleep", "خواب 🛌"),
        ChatKeypadBuilder().button("wave", "دست تکان دادن 👋"),
        ChatKeypadBuilder().button("fire", "آتش 🔥")
    )
    .row(
        ChatKeypadBuilder().button("epic_story", "📜 داستان پویای ایموجی")
    )
    .build()
)

animations = {
    "bird": ["🐦", "🐤", "🦉", "🕊️", "🐔"],
    "heart": ["❤️", "💖", "💘", "💕", "💞"],
    "flower": ["🌸", "🌷", "🌹", "🌺", "🌻"],

    "walk": ["🚶‍♂️", "🚶‍♀️", "🚶‍♂️", "🚶‍♀️", "🚶‍♂️"],
    "run": ["🏃‍♂️", "🏃‍♀️", "🏃‍♂️", "🏃‍♀️", "🏃‍♂️"],
    "car": ["🚗", "🚙", "🚕", "🚓", "🚗"],

    "cat": ["🐱", "😺", "😸", "😹", "😻"],
    "dog": ["🐶", "🐕", "🐩", "🐕‍🦺", "🐶"],
    "fish": ["🐟", "🐠", "🐡", "🦈", "🐟"],

    "rocket": ["🚀", "🛰️", "🌌", "🌠", "🚀"],
    "dance": ["💃", "🕺", "💃", "🕺", "💃"],
    "clap": ["👏", "🙌", "👏", "🙌", "👏"],

    "sleep": ["😴", "🛌", "💤", "😪", "😴"],
    "wave": ["👋", "🤚", "🖐️", "✋", "👋"],
    "fire": ["🔥", "💥", "🔥", "💥", "🔥"],

    "epic_story": [
        "🌅 صبح خوب شروع شد...",
        "🐓 قوقولی قوقو، پرنده بیدار شد",
        "🌄 خورشید طلوع کرد",
        "☕ وقت قهوه است!",
        "👩‍💻 شروع به کار با لپتاپ",
        "⌨️ تایپ تایپ تایپ...",
        "💡 یک ایده جدید به ذهن رسید",
        "🚶‍♂️ وقت پیاده‌روی کوتاه",
        "🌳 زیر درخت نشستم",
        "🐿️ سنجاب بازیگوش رو دیدم",
        "😄 لبخند زدم",
        "📱 گوشی رو چک کردم",
        "📧 ایمیل‌ها پر شده بودن",
        "🔥 کارها رو سریع انجام دادم",
        "🚴‍♂️ دوچرخه‌سواری رفتم",
        "🌬️ باد ملایم می‌وزید",
        "🌸 گل‌ها شکوفه داده بودند",
        "🌈 رنگین‌کمان زیبا در آسمان",
        "🌙 شب رسید، ماه روشن شد",
        "⭐ ستاره‌ها چشمک می‌زدن",
        "🌌 احساس آرامش می‌کردم",
        "📖 کتاب مورد علاقه‌ام رو خوندم",
        "😴 کم‌کم خوابم می‌آمد",
        "💤 خوب خوابیدم و آماده روز جدید شدم",
        "⏰ زنگ ساعت به صدا درآمد",
        "🌞 روز جدید آغاز شد",
        "🔄 و داستان دوباره شروع می‌شود...",
        "✨ زندگی پر از لحظه‌های زیباست",
        "❤️ ممنون که همراهی کردی!",
        "🎉 پایان داستان"
    ],
}

@bot.on_message()
def handle(bot, message: Message):
    btn_id = getattr(message.aux_data, "button_id", None)

    if message.text == "/start":
        message.reply_keypad("سلام! یکی از انیمیشن‌ها یا داستان‌ها رو انتخاب کن:", keypad=main_keypad)
        return

    if btn_id in animations:
        sent = message.reply(f"شروع {btn_id}...")
        message_id = sent["data"]["message_id"]
        chat_id = message.chat_id

        def animate():
            loops = 1 if btn_id == "epic_story" else 10
            for _ in range(loops):
                for frame in animations[btn_id]:
                    try:
                        bot.edit_message_text(chat_id, message_id, frame)
                        time.sleep(1 if btn_id == "epic_story" else 0.4)
                    except Exception:
                        return
            try:
                end_text = "داستان به پایان رسید! 🎬" if btn_id == "epic_story" else f"انیمیشن {btn_id} به پایان رسید!"
                bot.edit_message_text(chat_id, message_id, end_text)
            except Exception:
                pass

        threading.Thread(target=animate, daemon=True).start()
        return

    message.reply("لطفا /start را بفرست تا انیمیشن‌ها و داستان نمایش داده شوند.")

if __name__ == "__main__":
    bot.run()
