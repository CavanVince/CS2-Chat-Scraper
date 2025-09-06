from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    async def handle_command(self, username, command, *args):
        pass

    @abstractmethod
    async def run(self):
        pass

    async def save(self):
        pass