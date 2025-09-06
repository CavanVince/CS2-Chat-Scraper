from typing import List, Literal, Set, Union, Dict
from enum import Enum, auto
import os
import json
from games.base_game import Game

CURRENT_DIR = os.path.dirname(__file__) 
METADATA_SAVE_DIR = os.path.join(CURRENT_DIR, "res")
metadata_save_filename = lambda username: f"{username}.dat"

class Card:
    def __init__(self, rank: str, suit: Literal["spade", "diamond", "club", "heart"]):
        self.rank = rank
        self.suit = suit

    @classmethod
    def from_json(cls, data: dict) -> "Card":
        return cls(data["rank"], data["suit"])
    
    def to_json(self) -> Dict:
        return {
            "rank": self.rank,
            "suit": self.suit
        }

    def __str__(self):
        match (self.rank):
            case 1:
                pretty_rank = "Ace"
            case 11:
                pretty_rank = "Jack"
            case 12:
                pretty_rank = "Queen"
            case 13:
                pretty_rank = "King"
            case _:
                pretty_rank = self.rank

        return f"{pretty_rank} of {self.suit.capitalize}s"
    
class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def to_json(self) -> List[Dict]:
        return [
            c.to_json() for c in self.cards
        ]
    
    @property
    def busted(self) -> bool:
        return any([v > 21 for v in self.values])

    @classmethod
    def from_json(cls, data: List[Dict]) -> "Hand":
        hand = cls()
        hand.cards = [Card.from_json(d) for d in data]
        return hand

    @property
    def values(self) -> List[int]:
        soft = 0
        hard = 0
        for card in self.cards:
            if card.rank == 1:
                soft += 1
                hard += 11
            else:
                hard += min(card.rank, 10)
        if soft:
            return (soft, hard)
        return (hard,)

class Deck:
    def draw(self, receiving_hand: List[Card]):
        ...

    def shuffle(self):
        ...

class Player:
    def __init__(self, username: str, balance: int = 50):
        self.username = username
        self.balance = balance
        self.hand: Hand = []

    def to_json(self) -> dict:
        return {
            "username": self.username,
            "balance": self.balance,
        }
    
    @classmethod
    def from_json(cls, data: dict) -> "Player":
        player = cls(data["username"], data["balance"])
        return player

    def save(self):
        if not os.path.exists(METADATA_SAVE_DIR):
            os.makedirs(METADATA_SAVE_DIR)
        
        with open(os.path.join(METADATA_SAVE_DIR, metadata_save_filename(self.username)), 'wb') as fp:
            fp.write(json.dumps(self.to_json()).encode("utf-8"))

    @classmethod
    def load(cls, username: str) -> "Player":
        if not os.path.exists(METADATA_SAVE_DIR):
            print(f"Failed to load player {username} from file. Does not exist, creating new player")
            return Player(username)
        with open(os.path.join(METADATA_SAVE_DIR, metadata_save_filename(username)), 'rb') as fp:
            data = json.loads(fp.read().decode("utf-8"))
        player = cls(data["username"], data["balance"])
        return player
        ...


class GameState(int, Enum):
    IN_GAME = auto()
    OUT_OF_GAME = auto()

class Blackjack(Game):
    def __init__(self, min_bet: int = 5, max_bet: int = 50):
        self.players: List[Player] = set()
        self.game_state = GameState.OUT_OF_GAME

        self.turn_number: int = 0

        self.max_bet = max_bet
        self.min_bet = min_bet

    async def run(self):
        pass

    async def handle_command(self, username, command, *args):
        match (command):
            case "bet" | "b":
                ...
            case "join" | "j":
                ...
            case "hit" | "h":
                ...
            case "stand" | "st":
                ...
            case "split" | "sp":
                ...
            case "double-down" | "dd":
                ...
            case "insurance" | "ins":
                ...
            case "leave":
                ...
            case "help":
                ...
            case _:
                ...

    def rotate_turn_order(self):
        self.turn_number += 1 if self.turn_number < len(self.players) - 1 else 0

        if self.turn_number == 0:
            print("Dealer's Turn")
        else:
            cur_player = self.players[self.turn_number-1]
            print(f"{cur_player.username}'{'s' if cur_player.username.endswith('s') else ''} turn")
            
    def save_player(self, player: Player):
        ...

    def hit(self, username: str):
        ...

    def join_game(self, username: str):
        if username in [p.username for p in self.players]:
            return
        
        player = Player.load(username)
        print(f"Player {username} balance: {player.balance}")
        self.players.append(player)

    def leave_game(self, username: str):
        self.players
        if username not in [p.username for p in self.players]:
            return

    def set_bet(self, username: str, value: int):
        if username not in [p.username for p in self.players]:
            self.join_game(username)
        match (self.game_state):
            case GameState.IN_GAME:
                print(f"Set {username}'{'s' if not username.endswith('s') else ''} bet to {value} starting on the next hand.")
            case GameState.OUT_OF_GAME:
                print(f"Set {username}'{'s' if not username.endswith('s') else ''} bet to {value}")