import logging
from datetime import datetime, timedelta
from typing import Callable, List, Dict
import asyncio

from rubka2 import Robot
from rubka2.context import Message, InlineMessage
from rubka2.button import InlineBuilder
from rubka2.keypad import ChatKeypadBuilder
from rubka2.jobs import Job

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Robot(token="توکن شما")
active_jobs: Dict[int, Job] = {}

class ButtonManager:
    def __init__(self):
        self.buttons: Dict[str, List[Callable[[], List[Dict]]]] = {
            "basic": [
                lambda: InlineBuilder().row(InlineBuilder().button_simple("simple", "🔘 ساده")).build(),
                lambda: InlineBuilder().row(InlineBuilder().button_camera_image("camera_img", "📷 عکس با دوربین")).build(),
                lambda: InlineBuilder().row(InlineBuilder().button_camera_video("camera_vid", "🎥 ویدیو با دوربین")).build(),
            ],
            "timer_controls": [
                lambda: InlineBuilder().row(InlineBuilder().button_simple("cancel_timer", "⏹️ لغو تایمر")).build(),
            ]
        }

    def get_all_buttons(self) -> List[Dict]:
        all_btns = []
        for funcs in self.buttons.values():
            for f in funcs:
                all_btns.append(f())
        return all_btns

    def get_buttons_by_group(self, group: str) -> List[List[Dict]]:
        return [f() for f in self.buttons.get(group, [])]

button_manager = ButtonManager()

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

async def countdown_edit(chat_id: str, message_id: str, duration_sec: int):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_sec)

    while True:
        now = datetime.now()
        if now >= end_time:
            try:
                await bot.edit_message_text(chat_id, message_id, "⏰ زمان تمام شد!")
                await bot.edit_inline_keypad(chat_id, message_id,
                    InlineBuilder().row(InlineBuilder().button_simple("null", "\(￣︶￣*\)")).build())
            except Exception as e:
                logger.error(f"خطا در ویرایش پیام پایان: {e}")
            break

        remaining = end_time - now
        text = (
            f"⏳ تایمر فعال است...\n"
            f"🕰 شروع: {start_time.strftime('%H:%M:%S')}\n"
            f"⏲ پایان: {end_time.strftime('%H:%M:%S')}\n"
            f"⌛ باقی‌مانده: {str(remaining).split('.')[0]}"
        )
        try:
            await bot.edit_message_text(chat_id, message_id, text)
        except Exception as e:
            logger.error(f"خطا در ویرایش پیام شمارش معکوس: {e}")
        await asyncio.sleep(1)

@bot.on_message()
async def handle_commands(bot: Robot, message: Message):
    text = message.text or ""
    user_id = message.sender_id
    chat_id = message.chat_id

    if text.startswith("/start"):
        keypad = build_delay_keypad()
        await message.reply_keypad(
            "سلام 👋\n"
            "یک زمان برای ارسال پیام انتخاب کنید:\n"
            f"📅 تاریخ و ساعت فعلی: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}",
            keypad
        )
        return

    if text.startswith("/timer"):
        parts = text.strip().split()
        if len(parts) != 2 or not parts[1].isdigit():
            return await message.reply("⚠️ لطفاً مدت زمان را به صورت صحیح وارد کنید. مثل: `/timer 30`", parse_mode="markdown")

        seconds = int(parts[1])
        if user_id in active_jobs:
            active_jobs.pop(user_id)

        await message.reply(
            f"⏳ تایمر {seconds} ثانیه‌ای شروع شد!\n"
            f"🕰 زمان شروع: {datetime.now().strftime('%H:%M:%S')}",
            inline_keypad=button_manager.get_buttons_by_group("timer_controls")[0]
        )

        async def after_delay():
            if user_id not in active_jobs:
                return
            await bot.send_message(chat_id, f"✅ تایمر {seconds} ثانیه‌ای تمام شد! ⏰")
            active_jobs.pop(user_id, None)

        job = Job(seconds, after_delay)
        active_jobs[user_id] = job
        return

    if text.startswith("/all"):
        for idx, btn_func in enumerate(button_manager.get_all_buttons(), start=1):
            try:
                await message.reply_inline(f"🔘 دکمه شماره {idx}:", inline_keypad=btn_func)
            except Exception as e:
                await message.reply(f"❌ خطا در ارسال دکمه شماره {idx}: {e}", is_rtl=True)

@bot.on_callback()
async def callback_delay(bot: Robot, message: Message):
    btn_id = message.aux_data.button_id
    user_id = message.sender_id

    if btn_id == "cancel":
        if user_id in active_jobs:
            active_jobs.pop(user_id)
            await message.reply("❌ همه ارسال‌های زمان‌بندی شده لغو شدند.")
        else:
            await message.reply("⚠️ شما هیچ ارسال زمان‌بندی شده‌ای ندارید.")
        return

    if not btn_id.startswith("delay_"):
        await message.reply("❌ دکمه نامعتبر است!")
        return

    seconds = int(btn_id.split("_")[1])
    if user_id in active_jobs:
        active_jobs.pop(user_id)

    sent_msg = await message.reply_inline(".", button_manager.get_buttons_by_group("timer_controls")[0])
    message_id = sent_msg["data"]["message_id"]

    asyncio.create_task(countdown_edit(message.chat_id, message_id, seconds))

    async def delayed_send():
        if user_id not in active_jobs:
            return
        await bot.send_message(
            message.chat_id,
            f"✅ کاربر {user_id} : زمان {seconds} ثانیه گذشت و دستور اجرا شد! ⏰"
        )
        active_jobs.pop(user_id, None)

    job = Job(seconds, delayed_send)
    active_jobs[user_id] = job

    await message.reply(
        f"⏳ ثبت شد! پیام شما پس از {seconds} ثانیه ارسال خواهد شد.\n"
        f"🕰 زمان شروع ثبت شده: {datetime.now().strftime('%H:%M:%S')}"
    )

@bot.on_inline_query()
async def handle_inline_query(bot: Robot, message: InlineMessage):
    btn_id = message.aux_data.button_id
    user_id = message.sender_id

    if btn_id == "cancel_timer":
        if user_id in active_jobs:
            active_jobs.pop(user_id)
            await message.reply("⏹️ تایمر لغو شد.")
        else:
            await message.reply("⏹️ تایمری برای لغو وجود ندارد.")
    else:
        await message.reply(f"✅ دکمه کلیک‌شده: {btn_id}")

if __name__ == "__main__":
    logger.info("بوت در حال اجراست ...")
    bot.run()
