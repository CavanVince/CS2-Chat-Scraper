import os
import time
import re
import requests
import json
from utils import CONSOLE_FILE, write_command
from games import blackjack, coinflip
from games.CaseGame import case_game


def listen(logFile):
    logFile.seek(0, os.SEEK_END)
    last_size = logFile.tell()

    while True:
        current_size = os.stat(logFile.name).st_size
        if current_size < last_size:
            logFile.seek(0, os.SEEK_SET)
            last_size = current_size

        line = logFile.readline()
        if not line:
            time.sleep(0.1)
            continue

        print(line.strip())
        parse(line)
        last_size = logFile.tell()


def parse(line):
    regex = re.search(
        r"\[(?:ALL|(?:C)?(?:T)?)\]\s+(.*)‎(?:﹫\w+)?\s*(?:\[DEAD\])?:(?:\s)?(\S+)?\s(.+)?",
        line,
        flags=re.UNICODE,
    )
    if regex:
        username = regex.group(1)
        command = regex.group(2)
        args = regex.group(3)
    else:
        username = ""
        command = ""
        args = ""

    match command:
        case "!blackjack":
            time.sleep(0.5)
            write_command(f"say {username} {command} {args}")
        case "!flip":
            time.sleep(0.5)
            coinflip.flip(username)
        case "!case":
            time.sleep(0.5)
            case_game.start(username, args)


if __name__ == "__main__":
    log_file = open(CONSOLE_FILE, "r", encoding="utf-8")
    db = "https://csfloat.com/api/v1/listings/price-list"
    try:
        response = requests.get(db)
        response.raise_for_status()

        prices = response.json()
        with open("skin_prices.json", "w") as f:
            json.dump(prices, f, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    try:
        while True:
            listen(log_file)
    except KeyboardInterrupt:
        print("galls gone")
