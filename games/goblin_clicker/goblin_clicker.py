import asyncio
import os
import shutil
from typing import List
from games.base_game import Game
from datetime import datetime, timezone
import json

from utils import say
from games.goblin_clicker.player import Player
from games.goblin_clicker.common import SAVE_FILE_DIR, SAVE_INTERVAL
from games.goblin_clicker.codecs import game_object_hook, GameEncoder

class GoblinClicker(Game):
    def __init__(self):
        if not os.path.exists(SAVE_FILE_DIR):
            print(f"Making save directory for goblin clicker at :{SAVE_FILE_DIR}")
            os.makedirs(SAVE_FILE_DIR)

        self.players: List[Player] = []

        self._last_saved = datetime.now(tz=timezone.utc)

        self.init_from_file()

    def init_from_file(self):
        try:
            save_file = os.path.join(SAVE_FILE_DIR, "goblin_clicker.dat")
            if os.path.exists(save_file):
                with open(save_file, 'r') as fp:
                    players = json.load(fp, object_hook=game_object_hook)
                self.players.extend(players)
        except Exception as err:
            new_filename = save_file.replace(".dat", f"{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.dat.bak")
            print(f"ERROR: failed to load goblin clicker data. Has it been corrupted? Moving file location to: {new_filename} to prevent overwritten data. {err}")
            shutil.copyfile(save_file, new_filename)

    def save(self):
        if not self.players:
            return
        save_file = os.path.join(SAVE_FILE_DIR, "goblin_clicker.dat")
        with open(save_file, 'w') as fp:
            json.dump(self.players, fp, cls=GameEncoder, indent=2)
        self._last_saved = datetime.now(tz=timezone.utc)

    async def run(self):
        while True:
            # autosave every SAVE_INTERVAL units
            if datetime.now(tz=timezone.utc) - SAVE_INTERVAL >= self._last_saved:
                print("saving")
                self.save()

            # eventually we could use deltatime here but i cant be fucked atm
            await asyncio.sleep(1)
            for player in self.players:
                player.tick()

    async def handle_command(self, username, command, *args):
        player = self._get_player(username)
        if not player and command != "start":
            await say(f"Unknown player {username}. Start your goblin clicker adventure with '!gc start'")
            return
        
        match command:
            case "start":
                if player:
                    await say(f"{username} you already have a hamlet! Use '!gc help' to get more commands")
                    await self._say_stats(player)
                    return
                
                player = self._get_player(username, create_if_not_found=True)
                await say(f"A new goblin hamlet was created for you, {username}")
                await self._say_stats(player)
            case "purchase" | "buy":
                self._handle_purchase(player)
            case "sell":
                ...
            case "status" | "check":
                await self._say_stats(player)

    def _handle_purchase(player: Player, building_type: str, *args):
        ...

    async def _say_stats(self, player: Player):
        await say(f"{player.username}'{'s' if not player.username.endswith('s') else ''} Resources -- {player.currency}")

    def _get_player(self, username: str, create_if_not_found: bool = False):
        for p in self.players:
            if p.username == username:
                return p
        if create_if_not_found:
            player = Player(username)
            self.players.append(player)
            return player
        return None