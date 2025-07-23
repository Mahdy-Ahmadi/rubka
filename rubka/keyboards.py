from typing import Dict, List

def create_simple_keyboard(buttons: List[List[str]]) -> Dict:
    """
    Create a simple chat keypad (keyboard) structure for Rubika.
    buttons: List of button rows, each row is a list of button texts.
    Example:
    [
        ["Button1", "Button2"],
        ["Button3"]
    ]
    """
    keyboard = {"rows": []}
    for row in buttons:
        keyboard["rows"].append({"buttons": [{"text": text} for text in row]})
    return keyboard
