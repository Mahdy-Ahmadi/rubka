from typing import Callable, Dict, Any
import functools

def on_message(func: Callable):
    """
    Decorator to handle incoming message updates from Rubika.
    Extracts message details and passes them to decorated function.
    """
    @functools.wraps(func)
    def wrapper(update: Dict[str, Any], bot: 'Robot'):
        message_data = {}
        if 'update' in update and update['update'].get('type') == 'NewMessage':
            msg = update['update']['new_message']
            message_data = {
                'chat_id': update['update']['chat_id'],
                'message_id': msg.get('message_id'),
                'text': msg.get('text'),
                'sender_id': msg.get('sender_id')
            }
        elif 'inline_message' in update:
            msg = update['inline_message']
            message_data = {
                'chat_id': msg.get('chat_id'),
                'message_id': msg.get('message_id'),
                'text': msg.get('text'),
                'sender_id': msg.get('sender_id')
            }
        if message_data:
            return func(bot=bot, **message_data)
    return wrapper
