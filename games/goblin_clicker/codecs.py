import json
from typing import Any, Dict, Type

from games.goblin_clicker.player import Player
from games.goblin_clicker.currency import Currency, CurrencyType
from games.goblin_clicker.buildings import Building, GoldMine, LumberMill, Farm, House


class GameEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Player):
            return {
                "__type__": "Player",
                "username": obj.username,
                "goblins": obj.goblins,
                "currency": obj.currency,
                "buildings": obj.buildings,
            }
        elif isinstance(obj, Currency):
            return {
                "__type__": "Currency",
                "resources": obj.resources,
            }
        elif isinstance(obj, Building):
            return {
                "__type__": obj.__class__.__name__,
                "level": obj.level,
            }
        elif isinstance(obj, CurrencyType):
            return obj.name
        return super().default(obj)


def game_object_hook(d: Dict[str, Any]) -> Any:
    if "__type__" not in d:
        return d

    t = d["__type__"]

    if t == "Player":
        p = Player(d["username"])
        p.goblins = d["goblins"]
        p.currency = d["currency"]  # object_hook handles nested Currency
        p.buildings = d["buildings"]  # object_hook handles nested Buildings
        return p

    elif t == "Currency":
        return Currency(d["resources"])

    elif t in {"GoldMine", "LumberMill", "Farm", "House"}:
        cls: Type[Building] = {
            "GoldMine": GoldMine,
            "LumberMill": LumberMill,
            "Farm": Farm,
            "House": House,
        }[t]
        return cls(
            level=d["level"],
        )

    return d
