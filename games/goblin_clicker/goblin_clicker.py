import asyncio
import os
import shutil
from functools import lru_cache
from typing import List
from games.base_game import Game
from datetime import datetime, timezone
import json

from utils import say
from games.goblin_clicker.player import Player
from games.goblin_clicker.currency import NotEnoughCurrencyError
from games.goblin_clicker.buildings import ProductionBuilding
from games.goblin_clicker.common import RES_DIR, SAVE_INTERVAL
from games.goblin_clicker.codecs import game_object_hook, GameEncoder

from logger import get_logger

logger = get_logger(__name__)


class GoblinClicker(Game):
    def __init__(self):
        if not os.path.exists(RES_DIR):
            logger.info(f"Making save directory for goblin clicker at :{RES_DIR}")
            os.makedirs(RES_DIR)

        self.players: List[Player] = []

        self._last_saved = datetime.now(tz=timezone.utc)

        self.load()

    def load(self):
        try:
            save_file = os.path.join(RES_DIR, "goblin_clicker.dat")
            if os.path.exists(save_file):
                with open(save_file, "r") as fp:
                    players = json.load(fp, object_hook=game_object_hook)["data"]

                logger.info(f"Loaded {len(players)} players' data from save file")
                self.players.extend(players)
        except Exception as err:
            new_filename = save_file.replace(
                ".dat",
                f"{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.dat.bak",
            )
            logger.error(
                f"ERROR: failed to load goblin clicker data. Has it been corrupted? Moving file location to: {new_filename} to prevent overwritten data. {err}"
            )
            shutil.copyfile(save_file, new_filename)

    def save(self):
        logger.debug("Beginning save process...")
        if not self.players:
            logger.debug("nothing to save")
            return
        save_file = os.path.join(RES_DIR, "goblin_clicker.dat")
        self._last_saved = datetime.now(tz=timezone.utc)
        with open(save_file, "w") as fp:
            json.dump(
                {"last_saved": self._last_saved.isoformat(), "data": self.players},
                fp,
                cls=GameEncoder,
                indent=2,
            )
        logger.debug(
            f"File saved. at {self._last_saved}. Next save: {self._last_saved + SAVE_INTERVAL}"
        )

    async def run(self):
        while True:
            # autosave every SAVE_INTERVAL units
            if datetime.now(tz=timezone.utc) - SAVE_INTERVAL >= self._last_saved:
                logger.info("autosaving goblin clicker data")
                self.save()

            # eventually we could use deltatime here but i cant be fucked atm
            logger.debug("Async sleep for 1")
            await asyncio.sleep(1)
            self.tick()

    def tick(self):
        logger.debug("tick")
        for player in self.players:
            logger.debug(f"ticking for player {player.username}")
            for building in player.buildings:
                logger.debug(f"ticking building {building.__class__.__name__}")
                player.currency += building.production_per_tick

    async def handle_command(self, username, command, *args):
        logger.debug(f"Handling command: {username} {command} {args}")
        player = self._get_player(username)
        if not player and command != "start":
            logger.debug(f"Unknown player {username}")
            await say(
                f"Unknown player {username}. Start your goblin clicker adventure with '!gc start'"
            )
            return

        match command:
            case "start":
                if player:
                    logger.debug(f"Player {username} already known")
                    await say(
                        f"{username} you already have a hamlet! If you are sure you want to restart, type '!gc start -r'. Otherwise, try '!gc help' for a list of commands."
                    )
                    return

                logger.debug("Creating new player")
                player = self._get_player(username, create_if_not_found=True)
                await say(f"A new goblin hamlet was created for you, {username}")
                await self._say_stats(player)
                logger.debug("New player created")
            case "upgrade" | "up" | "ug" | "u":
                if len(args) < 1:
                    await say(
                        "You must supply the name of the building you wish to upgrade. ex. '!gc upgrade goldmine'"
                    )
                    return

                building_name, args = args[0], args[1:]
                building = player.get_building_by_name(building_name)
                if not building:
                    logger.debug(f"Did not find building to upgrade: {building_name}")
                    await say(f"No building was found by name: {building_name}")
                    return
                logger.debug(
                    f"Found building to upgrade: {building.__class__.__name__}"
                )
                await self._handle_upgrade(player, building, *args)
            case "status" | "check" | "" | None:
                if player is None:
                    await self._help_menu(player, *args)
                else:
                    await self._say_stats(player, *args)
            case "help":
                await self._help_menu(player, *args)

    async def _help_menu(self, player: Player, *args):
        for line in self.get_help_menu():
            await say(line)

    @lru_cache
    def get_help_menu(self):
        with open(os.path.join(RES_DIR, "help_menu.txt"), "r") as fp:
            return fp.readlines()

    async def _say_stats(self, player: Player, *args):
        un_str = f"{player.username}'{'s' if not player.username.endswith('s') else ''}"
        # long format
        if len(args) > 0 and args[0] == "-l":
            await say(f"{un_str} Resources -- {player.currency}")
            for building in player.buildings:
                prefix = ""
                if building.can_upgrade() and player.currency >= building.cost_to_upgrade:
                    prefix = "(Upgradeable) "
                elif not building.can_upgrade():
                    prefix = "(Max) "
                await say(f"{prefix}{str(building)}")
        else:
            await say(f"{player.username} - {player.currency.short_string()}")
            for building in player.buildings:
                prefix = ""
                if building.can_upgrade() and player.currency >= building.cost_to_upgrade:
                    prefix = "(Upgradeable) "
                elif not building.can_upgrade():
                    prefix = "(Max) "
                await say(f"{prefix}{building.short_string()}")

    async def _handle_upgrade(
        self, player: Player, building: ProductionBuilding, *args
    ):
        logger.debug(
            f"Handling upgrade {player.username} for {building.__class__.__name__}"
        )
        if player.currency < building.cost_to_upgrade:
            await say(
                f"Not enough resources to upgrade {building.__class__.__name__}, requires: {building.cost_to_upgrade}"
            )
            return

        async def upgrade() -> bool:
            try:
                building.upgrade(player.currency)
                logger.debug(
                    f"Upgraded {building.__class__.__name__} to level {building.level}. {player.currency}"
                )
            except NotEnoughCurrencyError:
                return False
            return True

        old_production = building.production_per_tick
        old_level = building.level

        if len(args) > 0 and args[0] == "-m":
            while building.can_upgrade() and await upgrade():
                pass
        else:
            await upgrade()
        await say(
            f"{building.__class__.__name__} upgraded from level {old_level} -> {building.level}. P/s: {old_production} -> {building.production_per_tick}"
        )
        await say(
            f"Remaining currency: {player.currency.short_string()}."
            + f" Required for next upgrade: {building.cost_to_upgrade.short_string()}"
            if building.can_upgrade()
            else ""
        )

    def _get_player(self, username: str, create_if_not_found: bool = False):
        for p in self.players:
            if p.username == username:
                return p
        if create_if_not_found:
            player = Player(username)
            self.players.append(player)
            return player
        return None
