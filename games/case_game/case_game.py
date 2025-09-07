from dataclasses import dataclass
import difflib
from functools import lru_cache
import json
import os
import random
import asyncio

from typing import Dict
from utils import write_and_send_command
from games.base_game import Game

CURRENT_DIR = os.path.dirname(__file__)
CASE_DATA_PATH = os.path.join(CURRENT_DIR, "res", "case_data.json")

COMMANDS = {
    "open": "Opening case...",
    "battle": "Starting battle...",
    "list": "Viewing cases...",
    "balance": "Checking balance...",
    "help": "Show commands...",
}

CASE_ODDS = {
    "Consumer Grade": 0.3,
    "Industrial Grade": 0.3,
    "Mil-Spec Grade": 0.2,
    "Restricted": 0.16,
    "Classified": 0.031,
    "Covert": 0.006,
    "Contraband": 0.003,
}


@dataclass
class Player:
    username: str
    _balance: float = 0

    @property
    def balance(self):
        return round(self._balance, 2)

    @balance.setter
    def balance(self, val: float):
        self._balance = val


class CaseGame(Game):
    def __init__(self):

        self.players: Dict[Player] = {}

    async def run(self):
        pass

    async def handle_command(self, username, command, *args):
        cmd = None
        match command:
            case "open":
                cmd = self.open_case
            case "battle":
                cmd = self.case_battle
            case "list":
                cmd = self.example_cases
            case "balance":
                cmd = self.check_balance
            case "help" | None | "":
                cmd = self.help_cmd
            case _:
              await write_and_send_command(
                    f"say Unknown command '{command}'. Type 'help' for commands."
                )
        if cmd is None:
            return
        print(f"Running command '{command}'")
        await cmd(username, *args)

    async def open_case(self, username, *args):
        player: Player = self.players.setdefault(username, Player(username))

        additional = 0.0
        case_name = " ".join(args)
        if not case_name:
            await write_and_send_command("say Usage: open <case name>")
            self.example_cases()
            return

        true_case_name, case = self.get_case(case_name)
        if not case:
            await write_and_send_command(f"say '{case_name}' is not a valid case.")
            self.example_cases()
            return
        
        await write_and_send_command(f"say {username} is opening {true_case_name}...")
        
        items_by_rarity = case.get("contains", {})
        present = {r: w for r, w in CASE_ODDS.items() if items_by_rarity.get(r)}
        if not present:
            await write_and_send_command("say Error: case has no items configured.")
            return

        # Adjust odds if low-tier if not souvenir
        if "Consumer Grade" not in present:
            additional += CASE_ODDS["Consumer Grade"]
        if "Industrial Grade" not in present:
            additional += CASE_ODDS["Industrial Grade"]

        if "Mil-Spec Grade" in present:
            present["Mil-Spec Grade"] += additional

        rarities = list(present.keys())
        weights = [present[r] for r in rarities]
        rarity = random.choices(rarities, weights=weights, k=1)[0]

        pool = items_by_rarity.get(rarity, [])
        if not pool:
            await write_and_send_command("say Error: rolled a rarity with no items.")
            return

        item = random.choice(pool)
        item_name = item.get("name", "Unknown Item")
        item_price = float(item.get("price", 0.0))
        player.balance += item_price

        await asyncio.sleep(0.5)
        await write_and_send_command(
            f"say {username} received: {item_name} ({rarity}). "
            f"${item_price:.2f} added to balance."
        )

    async def case_battle(self, username, *args):
      await write_and_send_command(f"say {COMMANDS['battle']}")

    async def check_balance(self, username, *args):
        balance = self.players.setdefault(username, Player(username)).balance
        await write_and_send_command(f"say {username}'s balance: ${balance:.2f}")

    async def help_cmd(self, *_):
        await write_and_send_command("say Commands: " + ", ".join(sorted(COMMANDS)))

    async def example_cases(self, *_):
        names = list(self.get_case_list().keys())
        first_3 = names[:3]
        suffix = "" if len(names) <= 3 else f" …and {len(names) - 3} more"
        await write_and_send_command(f"say Example cases: {', '.join(first_3)}{suffix}")

    @lru_cache
    def get_case_list(self):
        """Return dict: case_name -> {type, contains, ...} (cached)."""
        with open(CASE_DATA_PATH, "r", encoding="utf-8") as f:
            return {
                case["name"]: {k: v for k, v in case.items() if k != "name"}
                for case in json.load(f)
            }

    def get_case(self, case_name: str):
        """Case-insensitive lookup by name."""
        cases = self.get_case_list()
        closest = difflib.get_close_matches(case_name, cases, n=1, cutoff=0.75)
        if not closest:
            alias_to_exact = {}
            for exact, meta in cases.items():
                alias = meta.get("alias", exact)
                alias_to_exact[alias] = exact
            closest = difflib.get_close_matches(
                case_name, alias_to_exact.keys(), n=1, cutoff=0.75
            )
            if not closest:
                return None, None
            case_name = alias_to_exact[closest[0]]
        else:
            case_name = closest[0]
        return case_name, cases[case_name]