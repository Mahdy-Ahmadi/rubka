"""
🔹 Synchronous Example
```python
from rubka import Robot, Message

bot = Robot(token="YOUR_BOT_TOKEN")

@bot.on_message(commands=["start", "help"])
def handle_start(bot: Robot, message: Message):
    message.reply("👋 Hello! Welcome to the Rubka bot (sync example).")

bot.run()
```

Explanation

Robot is created with your bot token.
@bot.on_message registers a handler for incoming messages.

The function handle_start runs synchronously (step by step, blocking).

message.reply sends a message back to the user immediately.

Finally, bot.run() starts the event loop and keeps the bot running.

This approach is simpler and best for small bots or basic logic where you don’t need concurrency.

🔹 Asynchronous Example
```python
import asyncio
from rubka.asynco import Robot, Message

bot = Robot(token="YOUR_BOT_TOKEN")

@bot.on_message(commands=["start", "help"])
async def handle_start(bot: Robot, message: Message):
    await message.reply("⚡ Hello! This is the async version of Rubka.")

async def main():
    await bot.run()

asyncio.run(main())
```
Explanation

Uses rubka.asynco.Robot for asynchronous operation.

The handler handle_start is defined with async def.

await message.reply(...) is non-blocking: the bot can process other tasks while waiting for Rubika’s response.

asyncio.run(main()) starts the async event loop.

This approach is more powerful and recommended for larger bots or when you:

Need to call external APIs.

Handle multiple long-running tasks.

Want better performance and scalability.

👉 In short:

Sync = simple, step-by-step, blocking.

Async = scalable, concurrent, non-blocking.
"""

from .api import Robot
from .rubino import Bot
from .exceptions import APIRequestError
from .rubino import Bot as rubino
from .tv import TV as TvRubika

__all__ = [
    "Robot",
    "on_message",
    "APIRequestError",
    "create_simple_keyboard",
]