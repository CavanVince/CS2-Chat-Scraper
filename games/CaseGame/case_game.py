from utils import write_command
from dataclasses import dataclass
import random, time, json
import difflib

# ---------- Cache ----------
_cases_cache = None  

# ---------- Context ----------
@dataclass
class Context:
    username: str
    args: list[str]       
    balance: float = 0.0 

# ---------- Commands & Odds ----------
commands = {
    "open": "Opening case...",
    "battle": "Starting battle...",
    "list": "Viewing cases...",
    "balance": "Checking balance...",
    "help": "Show commands..."
}

case_odds = {
    "Consumer Grade": 0.3,
    "Industrial Grade": 0.3,
    "Mil-Spec Grade": 0.2,
    "Restricted": 0.16,
    "Classified": 0.031,
    "Covert": 0.006,
    "Contraband": 0.003,
}

# ---------- Core Actions ----------
def open_case(context: Context):
    additional = 0.0
    case_name = context.args[1].strip() if len(context.args) > 1 else ""
    if not case_name:
        write_command("say Usage: open <case name>"); example_cases(); return

    case = get_case(case_name)
    if not case:
        guess = case_guess(case_name)
        if not guess:
            write_command(f"say '{case_name}' is not a valid case."); example_cases(); return
        print(guess + " was the closest match")
        case = get_case(guess)
        case_name = case.get("name", guess)
    write_command(f"say {context.username} is opening {case_name}...")
    items_by_rarity = case.get("contains", {})

    present = {r: w for r, w in case_odds.items() if items_by_rarity.get(r)}
    if not present:
        write_command("say Error: case has no items configured."); return

    # Adjust odds if low-tier if not souvenir
    if "Consumer Grade" not in present:
        additional += case_odds["Consumer Grade"]
    if "Industrial Grade" not in present:
        additional += case_odds["Industrial Grade"]

    if "Mil-Spec Grade" in present:
        present["Mil-Spec Grade"] += additional
        
    rarities = list(present.keys())
    weights = [present[r] for r in rarities]
    rarity = random.choices(rarities, weights=weights, k=1)[0]

    pool = items_by_rarity.get(rarity, [])
    if not pool:
        write_command("say Error: rolled a rarity with no items."); return

    item = random.choice(pool)
    item_name = item.get("name", "Unknown Item")
    item_price = float(item.get("price", 0.0))
    context.balance += item_price

    time.sleep(0.5)
    write_command(f"say {context.username} received: {item_name} ({rarity}). "
                  f"${item_price:.2f} added to balance.")

def case_guess(case : str):
    cases = get_case_list()
    closest = difflib.get_close_matches(case, cases.keys(), n=1, cutoff=0.75)
    if not closest:
        alias_to_exact = {}
        for exact, meta in cases.items():
            alias = meta.get("alias", exact)
            alias_to_exact[alias] = exact
        closest = difflib.get_close_matches(case, alias_to_exact.keys(), n=1, cutoff=0.75)
        return alias_to_exact[closest[0]] if closest else None
    return closest[0] if closest else None

def case_battle(context: Context):
    write_command(f"say {commands['battle']}")

def check_balance(context: Context):
    write_command(f"say {context.username}'s balance: ${context.balance:.2f}")

def help_cmd():
    write_command("say Commands: " + ", ".join(sorted(commands)))

def example_cases():
    names = list(get_case_list().keys())
    first_3 = names[:3]
    suffix = "" if len(names) <= 3 else f" …and {len(names) - 3} more"
    write_command(f"say Example cases: {', '.join(first_3)}{suffix}")

# ---------- Data Loading ----------
def open_json_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_case_list():
    """Return dict: case_name -> {type, contains, ...} (cached)."""
    global _cases_cache
    if _cases_cache is None:
        cases = open_json_file("games/CaseGame/case_data.json")
        _cases_cache = {
            case["name"]: {k: v for k, v in case.items() if k != "name"}
            for case in cases
        }
    return _cases_cache

def get_case(case_name: str):
    """Case-insensitive lookup by name."""
    lookup = get_case_list()
    case = lookup.get(case_name)
    if case is not None:
        return case
    lc = case_name.lower()
    return next((v for k, v in lookup.items() if k.lower() == lc), None)

# ---------- Entry Point ----------
def start(username: str, args: str):
    if not args:
        help_cmd()
        return
 
    if not args:
        help_cmd()
        return
    parts = args.split(" ",1)
    command = parts[0].strip().lower()
    rest = parts[1].strip() if len(parts) > 1 else ""

    context = Context(username=username, args=[command, rest])

    match command:
        case "open":
            open_case(context)
        case "battle":
            case_battle(context)
        case "list":
            example_cases()
        case "balance":
            check_balance(context)
        case "help":
            help_cmd()
        case _:
            write_command(f"say Unknown command '{command}'. Type 'help' for commands.")

if __name__ == "__main__":
    start("test_user", "open Atlanta 2017 Dust II Souvenir Package")
