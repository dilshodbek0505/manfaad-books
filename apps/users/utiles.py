import random
import string
import requests


def generate_code():
    return ''.join(random.choices(string.digits, k=6))


def generate_token():
    return ''.join(random.choices(string.ascii_letters, k=32))


def sent_code_with_telegram(chat_id: int, code: str,):
    token = "5362566859:AAHw5aFl_azkCU2fE3iir2LEXpWDnNTYph8"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={code}"
    print(url)
    response = requests.post(url=url)