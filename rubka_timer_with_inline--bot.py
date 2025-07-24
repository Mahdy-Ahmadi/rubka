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
