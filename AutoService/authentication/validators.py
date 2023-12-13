from django.core import validators
import re

class NumberValidator(validators.RegexValidator):
    NUMBER_REGEX = "(25|29|33|44)[0-9]{7}"

    regex = re.compile(NUMBER_REGEX)