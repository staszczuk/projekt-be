import re


def extract_digits(str):
    digits = re.findall(r"\d+[\.,]?\d*", str)
    return "".join(digits)
