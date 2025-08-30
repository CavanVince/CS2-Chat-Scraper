import time
import re
import os
import pyautogui
from dotenv import load_dotenv
from games import *

load_dotenv()

CONSOLE_FILE = os.getenv('CONSOLE_FILE')
EXEC_FILE = os.getenv('EXEC_FILE')

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
            print(username, command, args)
            write_command(f"say {username} {command} {args}")
            press_key()
        case "!flip":
            ...



def write_command(command):
    with open(EXEC_FILE, 'w', encoding='utf-8') as f:
        f.write(command)

def press_key():
    time.sleep(0.2)
    pyautogui.press('=')


if __name__ == '__main__':
    log_file = open(CONSOLE_FILE,"r", encoding="utf-8")
    try:
        while True:
            listen(log_file)
    except KeyboardInterrupt:
        print("galls gone")