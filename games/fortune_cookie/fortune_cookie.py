from typing import List
from utils import say, gen_unique_nums
from dataclasses import dataclass
import random
import os
from games.base_game import Game

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


class FortuneCookie(Game):
    def __init__(self):
        
        self.lessons = []
        with open(LESSONS_FILEPATH, "r", encoding="utf-8") as fp:
            lesson = None
            for i, line in enumerate(fp.readlines()):
                line = line.replace("\n", "")
                if i % 3 == 0:
                    if lesson:
                        self.lessons.append(lesson)
                    lesson = Lesson(None, None, line)
                elif i % 3 == 1:
                    lesson.chinese = line
                elif i % 3 == 2:
                    lesson.pronunciation = line
            self.lessons.append(lesson)

        with open(PROVERBS_FILEPATH, "r") as fp:
            self.proverbs = fp.readlines()

    async def run():
        pass

    async def handle_command(self, username, *args):
        fortune = Fortune(
            random.choice(self.proverbs),
            Lotto(gen_unique_nums()),
            random.choice(self.lessons),
        )

        await say("-" * 68)
        await say(f"{username.capitalize()}'s fortune cookie says: {fortune.message}")
        await say(f"Lucky numbers: {fortune.lotto.numbers}")
        await say(
            f"{fortune.lesson.chinese} ({fortune.lesson.pronunciation}) -- {fortune.lesson.english}"
        )
        await say("-" * 68)
