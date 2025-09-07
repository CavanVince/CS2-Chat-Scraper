from typing import List

from games.goblin_clicker.buildings import Building, GoldMine, LumberMill, Farm
from games.goblin_clicker.currency import Currency, CurrencyType

class Player:
    def __init__(self, username):
        self.username = username
        self.goblins = 2

        self.buildings: List[Building] = [
            GoldMine(),
            LumberMill(),
            Farm()
        ]

        self.currency = Currency({
            CurrencyType.GOLD: 0,
            CurrencyType.LUMBER: 0,
            CurrencyType.FOOD: 0
        })

    def get_building_by_name(self, building_name: str):
        match building_name.lower():
            # this should really be more robust and not so "magic number" indexed, but that's a later problem
            case "gold" | "goldmine" | "mine":
                return self.buildings[0]
            case "wood" | "lumber" | "lumbermill" | "mill":
                return self.buildings[1]
            case "food" | "farm":
                return self.buildings[2]
            case _:
                return None
        

    
