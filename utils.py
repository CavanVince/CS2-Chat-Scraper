import time
import os
import pyautogui
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

CONSOLE_FILE = os.getenv('CONSOLE_FILE')
EXEC_FILE = os.getenv('EXEC_FILE')

def write_comand(command, write_mode: str = 'w'):
    with open(EXEC_FILE, write_mode, encoding='utf-8') as f:
        f.write(f"{command}{'\n' if write_mode == 'a' else ''}")

def say(text: str, **kwargs):
    write_comand(f"say {text}", **kwargs)

def say_once(text: str, **kwargs):
    say(text, **kwargs)
    press_key()

def press_key():
    time.sleep(0.2)
    pyautogui.press('=')

def write_and_send_command(command, **kwargs):
    write_comand(command, **kwargs)
    press_key()

@dataclass
class Metadata:
    map_name: str = None