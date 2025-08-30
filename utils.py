import time
import os
import pyautogui
from dotenv import load_dotenv

load_dotenv()

CONSOLE_FILE = os.getenv('CONSOLE_FILE')
EXEC_FILE = os.getenv('EXEC_FILE')


def write_command(command):
    with open(EXEC_FILE, 'w', encoding='utf-8') as f:
        f.write(command)
    press_key()

def press_key():
    time.sleep(0.2)
    pyautogui.press('=')