from games.goblin_clicker.currency import Cost, CurrencyType, Currency, NotEnoughCurrencyError
from games.goblin_clicker.common import GROWTH_RATE

class Building:
    def __init__(
        self, base_build_cost: Cost, base_production: Currency, level: int = 1
    ):
        self.base_build_cost = base_build_cost
        self.base_production = base_production

        self.level = level

        self._cached_cost_to_upgrade: Currency = None
        self._cached_production_per_tick: Currency = None

        self.max_level = 100

    @property
    def efficiency(self) -> float:
        # eventually this will reflect how many "workers" are occupying the building. If a gold mine can house 5 goblins but only 3 are working it, its efficiency would be 60% or 0.6
        return 1.0

    @property
    def cost_to_upgrade(self) -> Cost:
        if not self._cached_cost_to_upgrade:
            self._cached_cost_to_upgrade = Cost(
                {
                    k: v * (GROWTH_RATE**self.level)
                    for k, v in self.base_build_cost.resources.items()
                }
            )
        return self._cached_cost_to_upgrade

    @property
    def production_per_tick(self):
        if not self._cached_production_per_tick:
            self._cached_production_per_tick = Currency(
                {
                    k: v * self.level * self.efficiency
                    for k, v in self.base_production.resources.items()
                }
            )
        return self._cached_production_per_tick

    def can_upgrade(self):
        return self.level + 1 <= self.max_level

    def upgrade(self, purchaser: Currency):
        if purchaser < self.cost_to_upgrade:
            raise NotEnoughCurrencyError()

        purchaser -= self.cost_to_upgrade

        self.level += 1

        self._cached_cost_to_upgrade = None
        self._cached_production_per_tick = None

    def __str__(self):
        s = f"{self.__class__.__name__} [Level - {self.level}]"
        if self.production_per_tick:
            s += f" [Rate of Production - {self.production_per_tick}]"
        if self.can_upgrade():
            s += f" [Upgrade Cost - {self.cost_to_upgrade}]"

        return s
    
    def short_string(self):
        if self.can_upgrade():
            prefix = "(Upgradeable) "
        elif self.level == self.max_level:
            prefix = "(Max) "
        else:
            prefix = ""
        return f"{prefix}[Lvl: {self.level}, P: {self.production_per_tick.short_string()}, Next Lvl: {self.cost_to_upgrade.short_string()}]"


class GoldMine(Building):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 10, CurrencyType.LUMBER: 15}),
            base_production=Currency({CurrencyType.GOLD: 1}),
            level=level,
        )


class LumberMill(Building):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 5, CurrencyType.LUMBER: 15}),
            base_production=Currency({CurrencyType.LUMBER: 1}),
            level=level,
        )


class Farm(Building):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 5, CurrencyType.LUMBER: 5}),
            base_production=Currency({CurrencyType.FOOD: 3}),
            level=level,
        )


class House(Building):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 10, CurrencyType.LUMBER: 10}),
            base_production=None,
            level=level,
        )
