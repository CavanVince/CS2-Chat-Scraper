from datetime import datetime
from dotenv import load_dotenv
import os
import curses
from curses import wrapper
from curses.textpad import Textbox

load_dotenv()
CONSOLE_FILE = os.getenv('CONSOLE_FILE')
EXEC_FILE = os.getenv('EXEC_FILE')


def send_cmd(cmd: str, username: str = "admin"):
    prnt_str = f"{datetime.now().strftime("%m/%d %H:%M:%S")}  [ALL] {username}\u200E: {cmd.strip()}\n".encode("utf-8")
    with open(CONSOLE_FILE, 'ab') as fp:
        fp.write(prnt_str)

def main(stdscr):
    stdscr.clear()

    win = curses.newwin(1, 40, 0, 0)
    tbox = Textbox(win)
    stdscr.refresh()

    while True:
        win.clear()
        win.refresh()
        stdscr.move(0,0)
        tbox.edit()
        text = tbox.gather()
        if text.strip().lower() in ("q", "quit"):
            break
        send_cmd(text)


if __name__ == "__main__":

    wrapper(main)

    # args = parse_args()

    # print(f"Type something to log to: {CONSOLE_FILE}")
    # print(f"\t'q' - quit")
    # try:
    #     get_input(username=args.username)
    # except KeyboardInterrupt:
    #     print("Done!")