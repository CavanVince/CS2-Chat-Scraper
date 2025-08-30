import os
import time
import re
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
    regex = re.search(r"\[(?:ALL|(?:C)?(?:T)?)\]\s+(.*)‎(?:﹫\w+)?\s*(?:\[DEAD\])?:(?:\s)?(\S+)?\s(\S+)?", line, flags=re.UNICODE)
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


if __name__ == '__main__':
    log_file = open(CONSOLE_FILE,"r", encoding="utf-8")
    try:
        while True:
            listen(log_file)
    except KeyboardInterrupt:
        print("galls gone")