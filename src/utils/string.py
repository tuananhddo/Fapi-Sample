import re

from pydantic import ValidationError


def check_special_characters(value):
    if re.search(r"[^\w\s]", value):
        raise ValueError("Text cannot contain special characters")
    return value

def check_strong_password(password):
    MIN_PASSWORD_LEN = 8
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%^&*()])"
    if len(password) < MIN_PASSWORD_LEN:
        raise ValueError(f"Password length must greater or equal {MIN_PASSWORD_LEN}")
    if not bool(re.match(pattern, password)):
        raise ValueError("Password must contain at least two characters ( one upper and one lower), one number and one special character !@#\$%^&*()")
    return password