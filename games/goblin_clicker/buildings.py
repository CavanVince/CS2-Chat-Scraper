from abc import ABC, abstractmethod
from dataclasses import dataclass

from games.goblin_clicker.common import GROWTH_RATE, ALHPA

@dataclass
class Building(ABC):
    base_cost: int
    level: int = 1
    base_production: int = 1
    max_level: int = 100

    on_upgrade: callable = None

    _production_per_tick: int = None
    _cost_to_upgrade: int = None

    @property
    def production_per_tick(self):
        if not self._production_per_tick:
            self._production_per_tick = (
                self.base_production
                * (self.level + 1) ** ALHPA
                * GROWTH_RATE**self.level
            )
        return self._production_per_tick

    @property
    def cost_to_upgrade(self):
        if not self._cost_to_upgrade:
            self._cost_to_upgrade = self.base_cost * GROWTH_RATE**self.level
        return self._cost_to_upgrade
    
    @abstractmethod
    def tick(self, qty: int = 1):
        raise NotImplementedError(self.__name__)

    def upgrade(self):
        if self.level + 1 >= self.max_level:
            print(f"Gold Vault has reached max level of {self.max_level}")
            return
        
        self.level += 1
        self._production_per_tick = None
        self._cost_to_upgrade = None

        if self.on_upgrade is not None:
            self.on_upgrade(self)

@dataclass
class GoldVault(Building):
    base_cost: int = 10


@dataclass
class Lumbermill(Building):
    base_cost: int = 5

@dataclass
class Farm(Building):
    base_cost: int = 5

@dataclass
class House(Building):
    base_cost: int = 5
    on_upgrade: callable
    _goblins_housed: int = None

    @property
    def goblins_housed(self):
        if not self._goblins_housed:
            self._goblins_housed = (
                self.base_production
                * (self.level + 1) ** ALHPA
                * GROWTH_RATE**self.level
            )
        return self._goblins_housed

    def upgrade(self):
        self._goblins_housed = None
        super().upgrade()