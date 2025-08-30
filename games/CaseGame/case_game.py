from utils import write_command, CONSOLE_FILE
from dataclasses import dataclass
import random
import time
import json

_cases_cache = None

@dataclass(frozen=True)
class Context:
    username: str
    args: list[str]
    

commands = {
        "open": "Opening case...",
        "battle": "Starting battle...",
        "cases": "Viewing cases...",
        "balance": "Checking balance..."
    }

def open_case(context : Context):
    if context.args[2] in get_case_list():
        write_command(f"say {context.username} is opening the {context.args[2]} case!")
        # Add logic to open the case
        
    else:
        write_command(f"say {context.args[2]} is not a valid case.")
        example_cases()
        

def case_battle(context : Context):
    print(commands["battle"])

def open_json_file(file_path: str):
    with open(file_path) as f:
        return json.load(f)

def get_case_list():
    global _cases_cache
    if _cases_cache is None:
        cases = open_json_file("games/CaseGame/case_data.json")
        _cases_cache = {
            case["name"]: {k: v for k, v in case.items() if k != "name"}
            for case in cases
        }
    return _cases_cache

def example_cases():
    first_3 = list(get_case_list().keys())[:3]
    write_command(f"say Example cases: {', '.join(first_3)}")

def check_balance(context : Context):
    print(commands["balance"])
    
def help():
    command_list = commands.keys()
    write_command(f"say Commands: {', '.join(command_list)}")

def start(username, args):
    print(f"Starting case game for {username} with args: {args}")
    args_array = args.split(" ")
    context = Context(username=username, args=args_array)
    command = context.args[0].lower()

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
            help()
        case _:
            write_command(f"say Unknown command '{command}'. Type '!case help' for a list of commands.")

if __name__ == "__main__":
    start("test_user", "!case Basic Case")