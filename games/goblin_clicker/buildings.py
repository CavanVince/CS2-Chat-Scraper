from games.goblin_clicker.currency import (
    Cost,
    CurrencyType,
    Currency,
    NotEnoughCurrencyError,
)
from games.goblin_clicker.common import GROWTH_RATE


class Building:
    def __init__(self, base_build_cost: Cost, level: int = 1):
        self.base_build_cost = base_build_cost
        self.level = level

        self._cached_cost_to_upgrade: Currency = None

        self.max_level = 100

    @property
    def cost_to_upgrade(self) -> Cost:
        if not self._cached_cost_to_upgrade:
            self._cached_cost_to_upgrade = Cost(
                {
                    k: int(v * (GROWTH_RATE**self.level))
                    for k, v in self.base_build_cost.resources.items()
                }
            )
        return self._cached_cost_to_upgrade

    def can_upgrade(self) -> bool:
        return self.level + 1 <= self.max_level

    def upgrade(self, purchaser: Currency) -> None:
        if purchaser < self.cost_to_upgrade:
            raise NotEnoughCurrencyError()

        purchaser -= self.cost_to_upgrade

        self.level += 1

        self._cached_cost_to_upgrade = None

    def __str__(self):
        s = f"{self.__class__.__name__} [Level - {self.level}]"
        if self.can_upgrade():
            s += f" [Upgrade Cost - {self.cost_to_upgrade}]"

        return s

    def short_string(self):
        return f"{self.__class__.__name__} [Lvl: {self.level}, Next Lvl: {self.cost_to_upgrade.short_string()}]"


class ProductionBuilding(Building):
    def __init__(
        self, base_build_cost: Cost, base_production: Currency, level: int = 1
    ):
        super().__init__(base_build_cost, level)
        self.base_production = base_production

        self._cached_production_per_tick: Currency = None

        self.efficiency: float = 1.0

    @property
    def production_per_tick(self) -> Currency:
        if not self._cached_production_per_tick:
            self._cached_production_per_tick = Currency(
                {
                    k: int(v * self.level * self.efficiency)
                    for k, v in self.base_production.resources.items()
                }
            )
        return self._cached_production_per_tick

    def upgrade(self, purchaser: Currency):
        super().upgrade(purchaser)
        self._cached_production_per_tick = None

    def __str__(self):
        s = f"{self.__class__.__name__} [Level - {self.level}] [Rate of Production - {self.production_per_tick}]"
        if self.can_upgrade():
            s += f" [Upgrade Cost - {self.cost_to_upgrade}]"

        return s

    def short_string(self):
        return f"{self.__class__.__name__} [Lvl: {self.level}, P: {self.production_per_tick.short_string()}, Next Lvl: {self.cost_to_upgrade.short_string()}]"


class GoldMine(ProductionBuilding):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 10, CurrencyType.LUMBER: 15}),
            base_production=Currency({CurrencyType.GOLD: 1}),
            level=level,
        )


class LumberMill(ProductionBuilding):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 5, CurrencyType.LUMBER: 15}),
            base_production=Currency({CurrencyType.LUMBER: 1}),
            level=level,
        )


class Farm(ProductionBuilding):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 5, CurrencyType.LUMBER: 5}),
            base_production=Currency({CurrencyType.FOOD: 3}),
            level=level,
        )


class StorageBuilding(Building):
    def __init__(self, base_build_cost, base_storage_capacity: Currency, level=1):
        super().__init__(base_build_cost, level)

        self.base_storage_capacity = base_storage_capacity


class House(StorageBuilding):
    def __init__(self, level: int = 1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 10, CurrencyType.LUMBER: 10}),
            base_storage_capacity=Currency({CurrencyType.GOBLINS: 2}),
            level=level,
        )


class GoldVault(StorageBuilding):
    def __init__(self, level=1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 50, CurrencyType.LUMBER: 75}),
            base_storage_capacity=Currency({CurrencyType.GOLD: 500}),
            level=level,
        )


class Lumberyard(StorageBuilding):
    def __init__(self, level=1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 75, CurrencyType.LUMBER: 50}),
            base_storage_capacity=Currency({CurrencyType.LUMBER: 500}),
            level=level,
        )


class GrainSilo(StorageBuilding):
    def __init__(self, level=1):
        super().__init__(
            base_build_cost=Cost({CurrencyType.GOLD: 75, CurrencyType.LUMBER: 75}),
            base_storage_capacity=Currency({CurrencyType.FOOD: 500}),
            level=level,
        )
