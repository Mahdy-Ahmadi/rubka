from rubka import Robot
from rubka.context import Message

bot = Robot(token="token")

guid_channel = "c0xABCDEF..."  # شناسه کانال مورد نظر

@bot.on_message()
def start_handler(bot: Robot, message: Message):
    if bot.check_join(guid_channel, message.chat_id):
        name = bot.get_name(message.chat_id)
        message.reply(f"سلام {name} 👋\nشما عضو کانال هستید ✅")
    else:
        name = bot.get_name(message.chat_id)
        message.reply(f"سلام {name} 👋\nشما عضو کانال نیستید ❌")
        
bot.run()

#چون روبیکا متودی برای دریافت ممبر ها نداره این متود با استفاده از یه اکانت واقعی روبیکا که داخل چنل شما ادمین هست کار میکنه
