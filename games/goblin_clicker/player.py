from typing import List

from games.goblin_clicker.buildings import Building, GoldVault, Lumbermill, Farm
from games.goblin_clicker.currency import Currency, CurrencyType

class Player:
    def __init__(self, username):
        self.username = username
        self.goblins = 2

        self.buildings: List[Building] = []

        self.currency = Currency({
            CurrencyType.GOLD: 0,
            CurrencyType.LUMBER: 0,
            CurrencyType.FOOD: 0
        })

    def tick(self, amt: int = 1):
        for b in self.buildings:
            b.tick()
        

    
