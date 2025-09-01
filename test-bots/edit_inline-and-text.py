import asyncio
from rubka.asynco import Robot,filters,Message
from rubka.button import InlineBuilder

bot = Robot(token="token")

inline_start = InlineBuilder().row(
    InlineBuilder().button_simple("1","🎲 شرط بندی"),
    InlineBuilder().button_simple("2","✂️ سنگ-کاغذ-قیچی")
).row(
    InlineBuilder().button_simple("3","💬 شناسه چت من")
).build()

inline_updated = InlineBuilder().row(
    InlineBuilder().button_simple("1","🟢 بازی جدید"),
    InlineBuilder().button_simple("2","🔴 بازی تصادفی")
).row(
    InlineBuilder().button_simple("3","📌 اطلاعات چت")
).build()


@bot.on_message(filters.is_command.start | filters.is_command.game | filters.is_command.help)
async def handle_text(bot: Robot, msg: Message):
  
    sent_msg = await bot.send_message(
        chat_id=msg.chat_id,
        text="سلام! یکی از گزینه‌های زیر را انتخاب کنید:",
        inline_keypad=inline_start
    )
  
    await asyncio.sleep(5)
  
    await bot.edit_inline_keypad(
        chat_id=msg.chat_id,
        message_id=sent_msg.data.message_id,
        inline_keypad=inline_updated,
        text="🎉 گزینه‌ها به‌روز شدند! حالا می‌توانید انتخاب جدیدی داشته باشید."
    )
  
asyncio.run(bot.run())
