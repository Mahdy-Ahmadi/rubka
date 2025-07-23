
# rubka

A Python library for interacting with the Rubika Bot API using the Robot class.

## Overview
rubka is a powerful and easy-to-use Python SDK designed to simplify building bots for the Rubika platform.
It supports sending messages, editing, polls, locations, contacts, keyboards, and managing bot commands with a clean and modern interface.

## Installation

```bash
pip install rubka
```

Or install from source:

```bash
git clone https://github.com/Mahdy-Ahmadi/rubka.git
cd rubka
pip install .
```

## Quick Start

```python
from rubka import Robot, on_message

bot = Robot(token="YOUR_BOT_TOKEN")

@on_message
def handle_message(bot, chat_id, message_id, text, sender_id):
    if text == "/start":
        bot.send_message(chat_id, "Hello! Welcome to rubka.")

updates = bot.get_updates(limit=10)
for update in updates.get("updates", []):
    handle_message(update, bot)
```

## API Reference

### Class: Robot

The main class to interact with Rubika Bot API.

#### Methods:

- **get_me()**

  Retrieve information about the bot.

  Returns: `dict` — Bot information object.

  Example:

  ```python
  info = bot.get_me()
  print(info)
  ```

- **send_message(chat_id: str, text: str, chat_keypad: dict = None, inline_keypad: dict = None, disable_notification: bool = False, reply_to_message_id: str = None, chat_keypad_type: str = None)**

  Send a message to a chat with optional keypads.

  Parameters:

  - `chat_id` — Chat identifier.
  - `text` — Message text.
  - `chat_keypad` — (Optional) Custom keypad attached to chat.
  - `inline_keypad` — (Optional) Inline keypad attached to message.
  - `disable_notification` — (Optional) Disable notification for the message (default False).
  - `reply_to_message_id` — (Optional) Message ID to reply to.
  - `chat_keypad_type` — (Optional) Type of keypad ("New" or "Removed").

  Returns: `dict` — Response including the sent message ID.

  Example:

  ```python
  bot.send_message(
      chat_id="12345",
      text="Welcome!",
      inline_keypad={
          "rows": [
              {
                  "buttons": [
                      {"id": "100", "type": "Simple", "button_text": "Add Account"}
                  ]
              }
          ]
      }
  )
  ```

- **send_poll(chat_id: str, question: str, options: list[str])**

  Send a poll to a chat.

  Parameters:

  - `chat_id` — Chat identifier.
  - `question` — Poll question text.
  - `options` — List of poll options.

  Returns: `dict` — Response with poll message ID.

  Example:

  ```python
  bot.send_poll(
      chat_id="12345",
      question="Do you like this bot?",
      options=["Yes", "No"]
  )
  ```

- **send_location(chat_id: str, latitude: str, longitude: str, disable_notification: bool = False, inline_keypad: dict = None, reply_to_message_id: str = None, chat_keypad_type: str = None)**

  Send a location to a chat.

  Parameters:

  - `chat_id` — Chat identifier.
  - `latitude` — Latitude coordinate.
  - `longitude` — Longitude coordinate.
  - `disable_notification` — (Optional) Disable notification.
  - `inline_keypad` — (Optional) Inline keypad.
  - `reply_to_message_id` — (Optional) Reply message ID.
  - `chat_keypad_type` — (Optional) Keypad type.

  Returns: `dict` — Response with message ID.

- **send_contact(chat_id: str, first_name: str, last_name: str, phone_number: str, chat_keypad: dict = None, disable_notification: bool = False, inline_keypad: dict = None, reply_to_message_id: str = None, chat_keypad_type: str = None)**

  Send a contact to a chat.

  Parameters:

  - `chat_id` — Chat identifier.
  - `first_name` — Contact's first name.
  - `last_name` — Contact's last name.
  - `phone_number` — Contact's phone number.

  Additional optional keypad and notification parameters.

  Returns: `dict` — Response with message ID.

- **get_chat(chat_id: str)**

  Get information about a chat.

  Parameters:

  - `chat_id` — Chat identifier.

  Returns: `dict` — Chat info object.

- **get_updates(offset_id: str = None, limit: int = None)**

  Get recent updates/messages sent to the bot.

  Parameters:

  - `offset_id` — (Optional) Start offset for updates.
  - `limit` — (Optional) Max number of updates to retrieve.

  Returns: `dict` — Updates list.

- **forward_message(from_chat_id: str, message_id: str, to_chat_id: str, disable_notification: bool = False)**

  Forward a message from one chat to another.

  Parameters:

  - `from_chat_id` — Source chat ID.
  - `message_id` — Message ID to forward.
  - `to_chat_id` — Target chat ID.
  - `disable_notification` — (Optional) Disable notification.

  Returns: `dict` — Response with new message ID.

- **edit_message_text(chat_id: str, message_id: str, text: str)**

  Edit the text of a previously sent message.

  Parameters:

  - `chat_id` — Chat ID.
  - `message_id` — Message ID to edit.
  - `text` — New text.

  Returns: `dict` — Response status.

- **edit_inline_keypad(chat_id: str, message_id: str, inline_keypad: dict)**

  Edit the inline keypad of a message.

  Parameters:

  - `chat_id` — Chat ID.
  - `message_id` — Message ID.
  - `inline_keypad` — New inline keypad structure.

  Returns: `dict` — Response status.

- **delete_message(chat_id: str, message_id: str)**

  Delete a message in a chat.

  Parameters:

  - `chat_id` — Chat ID.
  - `message_id` — Message ID.

  Returns: `dict` — Response status.

- **set_commands(bot_commands: list[dict])**

  Set the list of bot commands for the bot menu.

  Parameters:

  - `bot_commands` — List of commands as dictionaries with "command" and "description".

  Returns: `dict` — Response status.

- **update_bot_endpoint(url: str, type: str)**

  Update the bot's webhook or API endpoint URL.

  Parameters:

  - `url` — New URL.
  - `type` — Type of update endpoint (e.g. "GetSelectionItem").

  Returns: `dict` — Response status.

- **remove_keypad(chat_id: str)**

  Remove keypad from a chat.

  Parameters:

  - `chat_id` — Chat ID.

  Returns: `dict` — Response status.

- **edit_chat_keypad(chat_id: str, chat_keypad: dict)**

  Edit or set a new keypad for a chat.

  Parameters:

  - `chat_id` — Chat ID.
  - `chat_keypad` — Keypad object.

  Returns: `dict` — Response status.

## Decorators

- **@on_message**

  Decorator for defining a message handler function.

  Automatically parses incoming updates and calls your handler with parameters: `bot, chat_id, message_id, text, sender_id`.

  Usage:

  ```python
  from rubka import on_message

  @on_message
  def my_handler(bot, chat_id, message_id, text, sender_id):
      # your code here
  ```

## Contributing

Contributions and feedback are welcome! Please submit issues or pull requests on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
