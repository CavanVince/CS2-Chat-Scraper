import json
from typing import Any, Dict, Type
from enum import Enum

from games.goblin_clicker.player import Player
from games.goblin_clicker.currency import Currency, CurrencyType
from games.goblin_clicker.buildings import Building, GoldVault, Lumbermill, Farm, House

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
                "base_cost": obj.base_cost,
                "level": obj.level,
                "base_production": obj.base_production,
                "max_level": obj.max_level,
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

    elif t in {"GoldVault", "Lumbermill", "Farm", "House"}:
        cls: Type[Building] = {
            "GoldVault": GoldVault,
            "Lumbermill": Lumbermill,
            "Farm": Farm,
            "House": House,
        }[t]
        return cls(
            base_cost=d["base_cost"],
            level=d["level"],
            base_production=d["base_production"],
            max_level=d["max_level"],
        )

    return d