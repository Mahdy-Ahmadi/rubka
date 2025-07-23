def is_valid_phone_number(phone: str) -> bool:
    """Simple phone number validation."""
    return phone.isdigit() and (10 <= len(phone) <= 15)
