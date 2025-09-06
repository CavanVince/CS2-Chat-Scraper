import time
import os
import pyautogui
import random
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
load_dotenv()

CONSOLE_FILE = os.getenv("CONSOLE_FILE")
EXEC_FILE = os.getenv("EXEC_FILE")


def write_command(command: str):
    with open(EXEC_FILE, "w", encoding="utf-8") as f:
        f.write(command)


async def say(text: str, **kwargs):
    write_command(f"say {text}", **kwargs)
    await press_key()


async def press_key():
    await asyncio.sleep(0.2)
    pyautogui.press("=")


def write_and_send_command(command, **kwargs):
    write_command(command, **kwargs)
    press_key()


def gen_unique_nums(amt: int = 5, lower_bound: int = 1, upper_bound: int = 100):
    nums = []
    while len(nums) < amt:
        num = random.randint(lower_bound, upper_bound)
        if num in nums:
            continue
        nums.append(num)
    return sorted(nums)


@dataclass
class Metadata:
    map_name: str = None
