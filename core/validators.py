from string import ascii_letters, digits

from rest_framework.exceptions import ValidationError


def password_validator(password):
    password_validation_errors = []
    character_count = digit_count = 0

    if len(password) < 6:
        password_validation_errors.append(
            "طول پسورد انتخابی بیش از حد کوتاه است."
        )

    for ch in password:
        if ch in ascii_letters:
            character_count += 1
        elif ch in digits:
            digit_count += 1

    if character_count == 0 or digit_count == 0:
        password_validation_errors.append(
            "پسورد انتخابی باید ترکیبی از حروف و اعداد باشد."
        )

    if password_validation_errors:
        raise ValidationError(password_validation_errors)
