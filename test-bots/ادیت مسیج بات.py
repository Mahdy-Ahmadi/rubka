import time
from rubka import Robot
from rubka.context import Message
bot = Robot(token="token")
@bot.on_message(commands=['start'])
def handle_salam(bot, message: Message):
    sent = message.reply("⏳ لطفاً صبر کنید...")
    time.sleep(1)
    bot.edit_message_text(
        chat_id=message.chat_id,
        message_id=sent['data']['message_id'],
        text="✅ سلام! خوش اومدی!"
    )
bot.run()
