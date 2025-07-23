from typing import Dict

from typing import Dict, List, Optional, Union
from typing import Dict, List, Optional

class InlineBuilder:
    def __init__(self):
        self.rows: List[Dict] = []

    def row(self, *buttons: Dict) -> "InlineBuilder":
        """
        افزودن یک ردیف دکمه به کیبورد
        حداقل یک دکمه باید داده شود.
        """
        if not buttons:
            raise ValueError("حداقل یک دکمه باید به row داده شود")
        self.rows.append({"buttons": list(buttons)})
        return self

    def button_simple(self, id: str, text: str) -> Dict:
        return {"id": id, "type": "Simple", "button_text": text}

    def button_selection(self, id: str, text: str, selection: Dict) -> Dict:
        """
        selection: dict با فیلدهای:
         - selection_id (str)
         - search_type (str) [ButtonSelectionSearchEnum: None, Local, Api]
         - get_type (str) [ButtonSelectionGetEnum: Local, Api]
         - items (list of ButtonSelectionItem)
         - is_multi_selection (bool)
         - columns_count (str)
         - title (str)
        """
        return {
            "id": id,
            "type": "Selection",
            "button_text": text,
            "button_selection": selection
        }

    def button_calendar(self, id: str, title: str, type_: str,
                        default_value: Optional[str] = None,
                        min_year: Optional[str] = None,
                        max_year: Optional[str] = None) -> Dict:
        """
        type_: ButtonCalendarTypeEnum = "DatePersian" | "DateGregorian"
        """
        calendar = {
            "title": title,
            "type": type_,
        }
        if default_value:
            calendar["default_value"] = default_value
        if min_year:
            calendar["min_year"] = min_year
        if max_year:
            calendar["max_year"] = max_year

        return {
            "id": id,
            "type": "Calendar",
            "button_text": title,
            "button_calendar": calendar
        }

    def button_number_picker(self, id: str, title: str, min_value: str, max_value: str,
                             default_value: Optional[str] = None) -> Dict:
        picker = {
            "title": title,
            "min_value": min_value,
            "max_value": max_value,
        }
        if default_value:
            picker["default_value"] = default_value

        return {
            "id": id,
            "type": "NumberPicker",
            "button_text": title,
            "button_number_picker": picker
        }

    def button_string_picker(self, id: str, title: Optional[str], items: List[str],
                             default_value: Optional[str] = None) -> Dict:
        picker = {
            "items": items
        }
        if default_value:
            picker["default_value"] = default_value
        if title:
            picker["title"] = title

        return {
            "id": id,
            "type": "StringPicker",
            "button_text": title if title else "انتخاب",
            "button_string_picker": picker
        }

    def button_location(self, id: str, type_: str, location_image_url: str,
                        default_pointer_location: Optional[Dict] = None,
                        default_map_location: Optional[Dict] = None,
                        title: Optional[str] = None) -> Dict:
        """
        type_: ButtonLocationTypeEnum = "Picker" | "View"
        location_image_url: str آدرس عکس دکمه موقعیت
        default_pointer_location و default_map_location هر کدام دیکشنری Location (latitude, longitude)
        """
        loc = {
            "type": type_,
            "location_image_url": location_image_url,
        }
        if default_pointer_location:
            loc["default_pointer_location"] = default_pointer_location
        if default_map_location:
            loc["default_map_location"] = default_map_location
        if title:
            loc["title"] = title

        return {
            "id": id,
            "type": "Location",
            "button_text": title if title else "موقعیت مکانی",
            "button_location": loc
        }

    def button_textbox(self, id: str, title: Optional[str], 
                       type_line: str, type_keypad: str,
                       place_holder: Optional[str] = None,
                       default_value: Optional[str] = None) -> Dict:
        """
        type_line: ButtonTextboxTypeLineEnum = "SingleLine" | "MultiLine"
        type_keypad: ButtonTextboxTypeKeypadEnum = "String" | "Number"
        """
        textbox = {
            "type_line": type_line,
            "type_keypad": type_keypad
        }
        if place_holder:
            textbox["place_holder"] = place_holder
        if default_value:
            textbox["default_value"] = default_value
        if title:
            textbox["title"] = title

        return {
            "id": id,
            "type": "Textbox",
            "button_text": title if title else "متن",
            "button_textbox": textbox
        }

    def button_payment(self, id: str, title: str, amount: int, description: Optional[str] = None) -> Dict:
        """
        نمونه‌ای ساده برای دکمه پرداخت (مقدار و توضیح دلخواه)
        """
        payment = {
            "title": title,
            "amount": amount
        }
        if description:
            payment["description"] = description

        return {
            "id": id,
            "type": "Payment",
            "button_text": title,
            "button_payment": payment
        }

    def button_camera_image(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "CameraImage",
            "button_text": title
        }

    def button_camera_video(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "CameraVideo",
            "button_text": title
        }

    def button_gallery_image(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "GalleryImage",
            "button_text": title
        }

    def button_gallery_video(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "GalleryVideo",
            "button_text": title
        }

    def button_file(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "File",
            "button_text": title
        }

    def button_audio(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "Audio",
            "button_text": title
        }

    def button_record_audio(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "RecordAudio",
            "button_text": title
        }

    def button_my_phone_number(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "MyPhoneNumber",
            "button_text": title
        }

    def button_my_location(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "MyLocation",
            "button_text": title
        }

    def button_link(self, id: str, title: str, url: str) -> Dict:
        return {
            "id": id,
            "type": "Link",
            "button_text": title,
            "url": url
        }

    def button_ask_my_phone_number(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "AskMyPhoneNumber",
            "button_text": title
        }

    def button_ask_location(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "AskLocation",
            "button_text": title
        }

    def button_barcode(self, id: str, title: str) -> Dict:
        return {
            "id": id,
            "type": "Barcode",
            "button_text": title
        }

    def build(self) -> Dict:
        return {"rows": self.rows}

from typing import List, Dict, Optional

class ChatKeypadBuilder:
    def __init__(self):
        self.rows: List[Dict[str, List[Dict[str, str]]]] = []

    def row(self, *buttons: Dict[str, str]) -> "ChatKeypadBuilder":
        """
        یک ردیف دکمه به کی‌پد اضافه می‌کند.
        ورودی: چند دیکشنری که نماینده دکمه‌ها هستند.
        """
        self.rows.append({"buttons": list(buttons)})
        return self

    def button(self, id: str, text: str, type: str = "Simple") -> Dict[str, str]:
        """
        دیکشنری یک دکمه می‌سازد.
        """
        return {"id": id, "type": type, "button_text": text}

    def build(
        self,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False
    ) -> Dict[str, object]:
        """
        ساختار نهایی chat_keypad را می‌سازد.
        """
        return {
            "rows": self.rows,
            "resize_keyboard": resize_keyboard,
            "on_time_keyboard": on_time_keyboard
        }
