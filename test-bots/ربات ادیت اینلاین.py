from rubka import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from rubka.jobs import Job
from datetime import datetime, timedelta
import threading
import time

bot = Robot("BEHDC0VVKCBRIBSCGVSTXDISIOFXMQWRJUCFDQTPAYACBTDYMPKPISPUSSPEYUIG")
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
