from datetime import datetime
from dotenv import load_dotenv
import os
from argparse import ArgumentParser

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument("-u", "--username", default="admin")

    return argparser.parse_args()

load_dotenv()

CONSOLE_FILE = os.getenv('CONSOLE_FILE')

def get_input(username: str):
    open(CONSOLE_FILE, 'w').close()
    while True:
        uin = input(">")
        if uin.lower() == "q" or uin.lower() == "quit":
            break
        
        prnt_str = f"{datetime.now().strftime("%m/%d %H:%M:%S")}  [ALL] {username}\u200E: {uin}\n"
        with open(CONSOLE_FILE, 'a', encoding="utf-8") as fp:
            fp.write(prnt_str)

if __name__ == "__main__":
    args = parse_args()

    print(f"Type something to log to: {CONSOLE_FILE}")
    print(f"\t'q' - quit")
    try:
        get_input(username=args.username)
    except KeyboardInterrupt:
        print("Done!")