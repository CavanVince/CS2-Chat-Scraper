from typing import List
from utils import write_and_send_command, press_key
from dataclasses import dataclass
import random
import os
import time

CURRENT_DIR = os.path.dirname(__file__)

PROVERBS_FILEPATH = os.path.join(CURRENT_DIR, "res", "proverbs.txt")
LESSONS_FILEPATH = os.path.join(CURRENT_DIR, "res", "lessons.txt")


@dataclass
class Lotto:
    numbers: List[int]


@dataclass
class Lesson:
    chinese: str
    pronunciation: str
    english: str


@dataclass
class Fortune:
    message: str
    lotto: Lotto
    lesson: Lesson


print("Loading Fortune cookie lessons and proverbs...")
LESSONS = []
with open(LESSONS_FILEPATH, "r", encoding="utf-8") as fp:
    lesson = None
    for i, line in enumerate(fp.readlines()):
        line = line.replace("\n", "")
        if i % 3 == 0:
            if lesson:
                LESSONS.append(lesson)
            lesson = Lesson(None, None, line)
        elif i % 3 == 1:
            lesson.chinese = line
        elif i % 3 == 2:
            lesson.pronunciation = line
    LESSONS.append(lesson)

with open(PROVERBS_FILEPATH, "r") as fp:
    PROVERBS = fp.readlines()


def write_fortune(username: str, fortune: Fortune):
    write_and_send_command("say " + ("-" * 68))
    write_and_send_command(
        f"say {username.capitalize()}'s fortune cookie says: {fortune.message}"
    )
    write_and_send_command(f"say Lucky numbers: {fortune.lotto.numbers}")
    write_and_send_command(f"say {fortune.lesson.chinese} ({fortune.lesson.pronunciation}) -- {fortune.lesson.english}")
    write_and_send_command("say " + ("-" * 68))


def gen_unique_nums(amt: int = 5, lower_bound: int = 1, upper_bound: int = 100):
    nums = []
    while len(nums) < amt:
        num = random.randint(lower_bound, upper_bound)
        if num in nums:
            continue
        nums.append(num)
    return sorted(nums)


def start(username: str, args: str):
    fortune = Fortune(
        random.choice(PROVERBS),
        Lotto(gen_unique_nums()),
        random.choice(LESSONS),
    )

    write_fortune(username, fortune)
