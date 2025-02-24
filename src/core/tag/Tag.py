import re
from datetime import datetime

class Tag:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class ValidatedTag(Tag):
    REGEX = None  # By default, no regex
    DATE_FORMAT = None  # By default, no date format

    def __init__(self, value: str):
        if not self.is_valid(value):
            ValueError(f"Invalid format: {value}")
        super().__init__(value)

    def __str__(self) -> str :
        return super().__str__()

    def is_valid(self, value: str|None = None) -> bool:
        if value == None :
            value = self.value
        if self.REGEX:  # If a regex is defined, use it
            return bool(self.REGEX.match(value))
        elif self.DATE_FORMAT:  # Otherwise, check the date
            try:
                datetime.strptime(value, self.DATE_FORMAT)
                return True
            except ValueError:
                return False
        return False  # No validation defined => always false


class CustomTag_email(ValidatedTag):
    REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class CustomTag_url(ValidatedTag):
    REGEX = re.compile(r'^(https?|ftp)://(?:[a-zA-Z0-9.-]+)(:[0-9]+)?(\/[^\s]*)?$')

class CustomTag_ISO8601_date(ValidatedTag):  # International Standard format (YYYY-MM-DD)
    DATE_FORMAT = "%Y-%m-%d"

class CustomTag_FR_date(ValidatedTag):  # French format (DD-MM-YYYY)
    DATE_FORMAT = "%d-%m-%Y"


'''# Exemples d'utilisation
try:
    email = CustomTag_email("test@example.com")
    print(f"Valid email: {email.value}")
except ValueError as e:
    print(e)

try:
    invalid_email = CustomTag_email("invalid-email")
except ValueError as e:
    print(e)

try:
    url = CustomTag_url("https://example.com")
    print(f"Valid URL: {url.value}")
except ValueError as e:
    print(e)

try:
    invalid_url = CustomTag_url("invalid-url")
except ValueError as e:
    print(e)

try:
    date = CustomTag_date("2024-02-10")
    print(f"Valid date: {date.value}")
except ValueError as e:
    print(e)

try:
    invalid_date = CustomTag_date("2024-13-40")
except ValueError as e:
    print(e)
'''