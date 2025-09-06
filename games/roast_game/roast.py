import os
import random
from utils import write_and_send_command, Metadata
import yaml
from games.base_game import Game

CURRENT_DIR = os.path.dirname(__file__)
ROAST_DATA_FILE = os.path.join(CURRENT_DIR, "res", "roasts.yaml")
roast_data = {}
if os.path.exists(ROAST_DATA_FILE):
    with open(ROAST_DATA_FILE, 'r') as fp:
        roast_data = yaml.safe_load(fp.read())

ALIASES = roast_data.get("aliases", {})
USER_SPECIFIC_ROASTS = roast_data.get("user-specific", {})

def random_nickname(name: str):
    return random.choice(ALIASES.get(name, []) + [name]).capitalize()

GENERAL_ROASTS = [
    lambda roastee, **__: f"Damn {random_nickname(roastee)}, even the bots are asking for a harder difficulty after watching you play!",
    lambda roastee, roaster: f"Watch out {random_nickname(roastee)}! {roaster.capitalize()} is coming to tickle you!",
    "Dork ass",
    lambda roastee, **__: f"Cash in those Steve Bucks {roastee}, it's all you got going for ya.",
    lambda roastee, **__: f"{random_nickname(roastee)} can't shoot for shit"
]

class Roast(Game):
    async def run(self):
        pass

    async def handle_command(self, username: str, *args):
        roastee = args[0]
        for a in ALIASES:
            if roastee in ALIASES[a]:
                roastee = a
                break

        roast_pool = [GENERAL_ROASTS]

        if user_pool := USER_SPECIFIC_ROASTS.get(roastee):
            roast_pool.append(user_pool)

        roast_pool = random.choice(roast_pool)
        selected_roast = random.choice(roast_pool)

        if not isinstance(selected_roast, str):
            selected_roast = selected_roast(roastee, roaster=username)
        await write_and_send_command(f"say | Roast Bot |: {selected_roast}")
