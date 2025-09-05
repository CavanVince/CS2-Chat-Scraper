import os
import time
import re
import requests
import json
from games.roast import roast
from utils import CONSOLE_FILE, write_and_send_command, Metadata
from games import coinflip
from games.CaseGame import case_game
from games.fortune_cookie import fortune_cookie

MAP_EXPR = re.compile(r"\[HostStateManager\] Host activate: Loading \((.*)\)")


def listen(filepath: str, **kwargs):
    with open(filepath, "r", encoding="utf-8") as fp:
        fp.seek(0, os.SEEK_END)
        last_size = fp.tell()

        while True:
            current_size = os.stat(fp.name).st_size
            if current_size < last_size:
                fp.seek(0, os.SEEK_SET)
                last_size = current_size

            line = fp.readline()
            if not line:
                time.sleep(0.1)
                continue

            print(line.strip())
            parse(line, kwargs=kwargs)
            last_size = fp.tell()


def parse(line, metadata: Metadata = None, **kwargs):
    if metadata is None:
        metadata = Metadata()

    r_match = re.search(
        r"\[(?:ALL|(?:C)?(?:T)?)\]\s+(.*)‎(?:﹫\w+)?\s*(?:\[DEAD\])?:(?:\s)?(\S+)?\s(.+)?",
        line,
        flags=re.UNICODE,
    )
    if not r_match:
        return

    username = r_match.group(1)
    command = r_match.group(2)
    args = r_match.group(3)

    match command:
        case "!blackjack":
            time.sleep(0.5)
            write_and_send_command(f"say {username} {command} {args}")
        case "!flip":
            time.sleep(0.5)
            coinflip.flip(username)
        case "!case":
            time.sleep(0.5)
            case_game.start(username, args)
        case "!roast":
            time.sleep(0.5)
            roast.start(username, args, metadata=metadata, **kwargs)
        case "!fortune-cookie" | "!fc" | "!fortune":
            time.sleep(0.5)
            fortune_cookie.start(username, args)


def reverse_readline(filename, buf_size=8192):
    with open(filename, "rb") as f:
        f.seek(0, 2)
        buffer = b""
        pointer = f.tell()
        while pointer > 0:
            read_size = min(buf_size, pointer)
            pointer -= read_size
            f.seek(pointer)
            data = f.read(read_size)
            buffer = data + buffer
            lines = buffer.split(b"\n")
            buffer = lines[0]
            for line in reversed(lines[1:]):
                yield line.decode("utf-8", errors="replace")
        if buffer:
            yield buffer.decode("utf-8", errors="replace")


def find_metadata(filename: str) -> Metadata:
    for line in reverse_readline(filename):
        if m := re.search(MAP_EXPR, line):
            map_name = m.group(1)
            break
    else:
        return

    map_name = map_name.split("_", 1)[1]
    return Metadata(map_name=map_name)


if __name__ == "__main__":
    metadata = find_metadata(CONSOLE_FILE)

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
            listen(CONSOLE_FILE, metadata=metadata)
    except KeyboardInterrupt:
        print("galls gone")
