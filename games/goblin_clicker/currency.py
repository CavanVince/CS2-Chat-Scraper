from typing import Dict
from dataclasses import dataclass, field

class NotEnoughCurrencyError(Exception): 
    pass

@dataclass
class CurrencyType:
    FOOD: str = "food"
    GOLD: str = "gold"
    LUMBER: str = "lumber"

@dataclass
class Currency:
    resources: Dict[str, int] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.resources.get(key, 0)

    def __add__(self, other: "Currency"):
        return Currency({
            res: self[res] + other[res]
            for res in set(self.resources) | set(other.resources)
        })

    def __sub__(self, other: "Currency"):
        return Currency({
            res: self[res] - other[res]
            for res in set(self.resources) | set(other.resources)
        })

    def __ge__(self, other: "Currency"):
        return all(self[res] >= other[res] for res in other.resources)
    
    def __gt__(self, other: "Currency"):
        return all(self[res] > other[res] for res in other.resources)

    def __le__(self, other: "Currency"):
        return all(self[res] <= other[res] for res in other.resources)
    
    def __lt__(self, other: "Currency"):
        return all(self[res] < other[res] for res in other.resources)

    def __eq__(self, other: "Currency"):
        return self.resources == other.resources
    
    def __str__(self):
        return ", ".join(f"{k.capitalize()}: {v:.0f}" for k, v in self.resources.items())
    
    def short_string(self):
        return ', '.join(f"{k[0].capitalize()}: {v:.0f}" for k, v in self.resources.items())

@dataclass
class Cost(Currency):
    def set_cost(self, cost: Dict[CurrencyType, int]):
        self.resources = cost

    def can_buy(self, money: Currency):
        return money >= self
