"""
🔹 Synchronous Example
```python
from rubka import Bot,Message

bot = Robot(token="YOUR_BOT_TOKEN")

@bot.on_message(commands=["start", "help"])
def handle_start(bot: Robot, message: Message):
    message.reply("👋 Hello! Welcome to the Rubka bot (sync example).")

bot.run()
```
🔹 Asynchronous Example
```python
from rubka import Robot, Message

bot = Robot(token="YOUR_BOT_TOKEN")

@bot.on_message(commands=["start", "help"])
async def handle_start(bot: Robot, message: Message):
    await message.reply("⚡ Hello! This is the async version of Rubka.")

bot.run()
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
import requests
from typing import Optional
try:
    from importlib.metadata import version, PackageNotFoundError
    use_importlib_metadata = True
except ImportError:
    import pkg_resources
    use_importlib_metadata = False
def get_installed_version(package_name: str) -> Optional[str]:
    if use_importlib_metadata:
        try:return version(package_name)
        except PackageNotFoundError:return None
    else:
        try:return pkg_resources.get_distribution(package_name).version
        except pkg_resources.DistributionNotFound:return None
def get_latest_version(package_name: str) -> Optional[str]:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("info", {}).get("version")
    except Exception as e:
        #print(f"Error fetching latest version: {e}")
        return None

def check_rubka_version():
    package_name = "rubka"
    installed_version = get_installed_version(package_name)
    if installed_version is None:
        print(f"{package_name} is not installed.")
        return
    latest_version = get_latest_version(package_name)
    if latest_version is None:
        print("Failed to fetch latest version info.")
        return
    if installed_version != latest_version:
        print("⚠️ **Warning: Outdated Version Detected!** ⚠️")
        print("This version poses potential risks to the stability, security, and compatibility of your system.")
        print(f"\n- Installed version: {installed_version}")
        print(f"- Latest available version: {latest_version}")
        print("\nImmediate action is required to ensure optimal performance and security.")
        print(f"To update, run the following command:")
        print(f"\n    pip install {package_name}=={latest_version}\n")
        print("For more details and updates, Channel : @rubka_info")
check_rubka_version()
from .asynco import Robot,Message,ChatKeypadBuilder,InlineBuilder,filters,InlineMessage
from .api import Robot as Bot,Message,InlineMessage
from .exceptions import APIRequestError
from .rubino import Bot as rubino
from .tv import TV as TvRubika

__all__ = [
    "Robot",
    "on_message",
    "APIRequestError",
    "create_simple_keyboard",
]
