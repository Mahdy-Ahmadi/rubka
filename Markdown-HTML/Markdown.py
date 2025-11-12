from rubka.asynco import Robot, Message

TOKEN = ""
bot = Robot(TOKEN)

@bot.on_message()
async def handle_message(bot: Robot, message: Message):
    html_text = f"""Hi {await message.name}
$Welcome to our amazing Rubka bot demo! 🎉
Here is a [Quote example](https://rubka.ir) that spans multiple lines,
and inside it you can see:
- **Bold text**
- __Italic text__
- --Underlined text--
- `Mono text`
- ~~Strikethrough~~
- ||Spoiler content||
$
Outside the quote, you can also highlight:

- **Important parts**  
- __Emphasized words__  
- Links like [Rubka](https://rubka.ir)  

> You can even show `inline code` or code blocks:

```from rubka.asynco import Robot,Message
bot = Robot("token")
@bot.on_message()
async def handle_start(bot: Robot, message: Message):
    await message.reply(f"Hello Word")
bot.run()```

Enjoy exploring all the Markdown features! ✨
"""
    await message.reply(html_text)

bot.run()
