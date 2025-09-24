import asyncio
import json
import logging
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from rubka.asynco import Robot
from rubka.button import ChatKeypadBuilder
from rubka.context import Message

token = ""

TOKEN = os.getenv("BOT_TOKEN", token)
CHARGE_API_URL = "https://api.rubka.ir/charge"
DATA_FILE = Path("data.json")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CallbackData:
    
    AMOUNT_PREFIX = "amount_"
    DAEMI_YES = "daemi_yes"
    DAEMI_NO = "daemi_no"
    SUPER_ON = "super_on"
    SUPER_OFF = "super_off"
    CONFIRM_SEND = "confirm_send"
    CANCEL_SEND = "cancel_send"

class Messages:
    
    WELCOME = "سلام! برای خرید شارژ، شماره تلفن خود را با فرمت 09xxxxxxxx وارد کنید."
    PHONE_SAVED = "شماره ثبت شد: {phone}\nلطفا مبلغ را انتخاب کنید:"
    AMOUNT_SELECTED = "مبلغ انتخاب شد: {amount:,} تومان\nآیا خط دائمی است؟"
    DAEMI_SELECTED = "خط دائمی: {is_daemi}\nنوع شارژ را انتخاب کنید:"
    ORDER_SUMMARY = (
        "خلاصه سفارش:\n"
        "شماره: {phone}\n"
        "مبلغ: {amount:,} تومان\n"
        "خط دائمی: {is_daemi}\n"
        "نوع: {charge_type}\n\n"
        "برای ارسال نهایی تایید کنید:"
    )
    REQUEST_IN_PROGRESS = "در حال ارسال درخواست..."
    PAYMENT_LINK = "لینک پرداخت شارژ: \n{url}\n\nپنج ثانیه پس از پرداخت، شارژ برای شما واریز خواهد شد."
    ORDER_CANCELED = "سفارش لغو شد."
    INVALID_STATE = "فرآیند نامعتبر است. لطفا با ارسال شماره تلفن مجددا شروع کنید (فرمت: 09xxxxxxxx)."
    API_ERROR = "خطا در تماس با سرویس شارژ: {error}"
    UNKNOWN_BUTTON = "دکمه شناخته نشد: {button_id}"


def build_keypads() -> Dict[str, list]:
    
    amounts = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
    amount_keypad = (
        ChatKeypadBuilder()
        .row(*[ChatKeypadBuilder().button(f"{CallbackData.AMOUNT_PREFIX}{a}", f"{a:,}") for a in amounts[:5]])
        .row(*[ChatKeypadBuilder().button(f"{CallbackData.AMOUNT_PREFIX}{a}", f"{a:,}") for a in amounts[5:]])
        .build()
    )
    daemi_keypad = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button(CallbackData.DAEMI_YES, "خط دائمی ✅"),
            ChatKeypadBuilder().button(CallbackData.DAEMI_NO, "خط عادی ❌"),
        )
        .build()
    )
    super_keypad = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button(CallbackData.SUPER_ON, "شگفت انگیز (Super) 🌟"),
            ChatKeypadBuilder().button(CallbackData.SUPER_OFF, "معمولی (Normal)"),
        )
        .build()
    )
    confirm_keypad = (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button(CallbackData.CONFIRM_SEND, "تایید و ارسال ✅"),
            ChatKeypadBuilder().button(CallbackData.CANCEL_SEND, "لغو ❌"),
        )
        .build()
    )
    return {
        "amount": amount_keypad,
        "daemi": daemi_keypad,
        "super": super_keypad,
        "confirm": confirm_keypad,
    }

KEYPADS = build_keypads()



@dataclass
class OrderState:
    
    phone: str
    amount: Optional[int] = None
    is_daemi: Optional[bool] = None
    is_super: Optional[bool] = None

    def get_summary(self) -> str:
        
        return Messages.ORDER_SUMMARY.format(
            phone=self.phone,
            amount=self.amount,
            is_daemi='بله' if self.is_daemi else 'خیر',
            charge_type='شگفت انگیز' if self.is_super else 'معمولی'
        )



def load_data() -> Dict[str, Any]:
    
    if not DATA_FILE.exists():
        return {"users": {}, "history": []}
    try:
        data = json.loads(DATA_FILE.read_text("utf-8"))
        data.setdefault("users", {})
        data.setdefault("history", [])
        return data
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load data file: {e}")
        return {"users": {}, "history": []}


def save_data(data: Dict[str, Any]):
    
    try:
        DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    except IOError as e:
        logger.error(f"Could not save data file: {e}")


def is_valid_phone(text: str) -> bool:
    
    return bool(re.match(r"^09\d{9}$", text.strip()))



async def purchase_charge(order: OrderState) -> Dict[str, Any]:
    
    params = {
        "phone": order.phone,
        "amount": order.amount,
        "type": "direct",
        "super": "on" if order.is_super else "off",
        "daemi": "yes" if order.is_daemi else "no",
    }
    
    def do_request():
        
        response = requests.get(CHARGE_API_URL, params=params, timeout=15)
        response.raise_for_status()  
        return response.json()

    return await asyncio.to_thread(do_request)



bot = Robot(TOKEN, web_hook=None)

pending_orders: Dict[str, OrderState] = {}


@bot.on_message(commands=["start"])
async def cmd_start(bot: Robot, message: Message):
    
    await message.reply(Messages.WELCOME)


@bot.on_message()
async def handle_phone_number(bot: Robot, message: Message):
    
    text = (message.text or "").strip()
    if not is_valid_phone(text):
        return  

    user_id = message.sender_id
    pending_orders[user_id] = OrderState(phone=text)

    
    data = load_data()
    data["users"].setdefault(user_id, {})["last_phone"] = text
    save_data(data)

    await message.reply(
        Messages.PHONE_SAVED.format(phone=text),
        chat_keypad=KEYPADS["amount"],
    )



async def handle_amount_selection(message: Message, user_id: str, order: OrderState):
    
    amount_str = message.aux_data.button_id.split(CallbackData.AMOUNT_PREFIX)[1]
    order.amount = int(amount_str)
    await message.answer(
        Messages.AMOUNT_SELECTED.format(amount=order.amount),
        chat_keypad=KEYPADS["daemi"]
    )

async def handle_daemi_selection(message: Message, user_id: str, order: OrderState):
    
    order.is_daemi = (message.aux_data.button_id == CallbackData.DAEMI_YES)
    is_daemi_text = 'بله' if order.is_daemi else 'خیر'
    await message.answer(
        Messages.DAEMI_SELECTED.format(is_daemi=is_daemi_text),
        chat_keypad=KEYPADS["super"]
    )

async def handle_super_selection(message: Message, user_id: str, order: OrderState):
    
    order.is_super = (message.aux_data.button_id == CallbackData.SUPER_ON)
    summary = order.get_summary()
    await message.reply_keypad(summary, keypad=KEYPADS["confirm"])


async def handle_cancellation(message: Message, user_id: str):
    
    pending_orders.pop(user_id, None)
    await message.answer(Messages.ORDER_CANCELED)


async def handle_confirmation(message: Message, user_id: str, order: OrderState):
    
    await message.answer(Messages.REQUEST_IN_PROGRESS)
    
    try:
        api_result = await purchase_charge(order)
        payment_url = api_result.get("paymentInfo", {}).get("paymentGateway", {}).get("url")
        
        if not payment_url:
            raise ValueError("Payment URL not found in API response.")

        
        data = load_data()
        data["history"].append({
            "user_id": user_id,
            "order": asdict(order),
            "api_response": api_result,
        })
        save_data(data)
        
        await message.answer(Messages.PAYMENT_LINK.format(url=payment_url))

    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error(f"API call failed for user {user_id}: {e}")
        await message.answer(Messages.API_ERROR.format(error=e))
    finally:
        
        pending_orders.pop(user_id, None)


@bot.on_callback()
async def callback_router(bot: Robot, message: Message):
    user_id = message.sender_id
    button_id = message.aux_data.button_id
    order = pending_orders.get(user_id)
    if not order:
        await message.answer(Messages.INVALID_STATE)
        return
    if button_id.startswith(CallbackData.AMOUNT_PREFIX):
        await handle_amount_selection(message, user_id, order)
    elif button_id in (CallbackData.DAEMI_YES, CallbackData.DAEMI_NO):
        await handle_daemi_selection(message, user_id, order)
    elif button_id in (CallbackData.SUPER_ON, CallbackData.SUPER_OFF):
        await handle_super_selection(message, user_id, order)
    elif button_id == CallbackData.CONFIRM_SEND:
        await handle_confirmation(message, user_id, order)
    elif button_id == CallbackData.CANCEL_SEND:
        await handle_cancellation(message, user_id)
    else:
        await message.answer(Messages.UNKNOWN_BUTTON.format(button_id=button_id))

if __name__ == "__main__":
    if not TOKEN or len(TOKEN) < 30:
        logger.critical("Bot token is missing or invalid! Please set the BOT_TOKEN environment variable.")
    else:
        logger.info("Bot is starting...")
        asyncio.run(bot.run())
