import asyncio
import os
import re

from games.case_game.case_game import CaseGame
from games.fortune_cookie.fortune_cookie import FortuneCookie
from games.goblin_clicker.goblin_clicker import GoblinClicker
from games.roast_game.roast import Roast
from utils import CONSOLE_FILE

from logger import get_logger, setup_logging
setup_logging()
logger = get_logger("main")


COMMAND_RE = re.compile(r"\[(?:ALL|(?:C)?(?:T)?)\]\s+(.*)‎(?:﹫\w+)?\s*(?:\[DEAD\])?:(?:\s)?(\!\S+)?\s(.+)?")

fortune_cookie = FortuneCookie()
case_game = CaseGame()
roast = Roast()
goblin_clicker = GoblinClicker()

async def command_dispatcher(command_queue: asyncio.Queue):
    logger = get_logger("main.command_dispatcher")
    while True:
        logger.debug("Waiting for queue...")
        username, service, command, *args = await command_queue.get()
        logger.debug(f"Command dispatcher received items to process! {username}, {service}, {command}, {args}")
        service, command = service.lower(), command.lower()
        
        svc = None
        match service:
            case "!fc" | "!fortune" | "!fortune-cookie":
                svc = fortune_cookie
            case "!case":
                svc = case_game
            case "!roast":
                svc = roast
            case "!gc" | "!goblin" | "!goblin-clicker" | "!clicker":
                svc = goblin_clicker
        if not svc:
            return
        logger.info(f"Handling request for service {service}")
        await svc.handle_command(username, command, *args)

async def poll_console_log(command_queue: asyncio.Queue):
    logger = get_logger("main.poll_console_log")
    with open(CONSOLE_FILE, "r", encoding="utf-8") as fp:
        fp.seek(0, os.SEEK_END)
        last_size = fp.tell()

        while True:
            logger.debug(f"Stat'ing file {fp.name}")
            current_size = os.stat(fp.name).st_size
            if current_size < last_size:
                fp.seek(0, os.SEEK_SET)
                last_size = current_size
            logger.debug("Reading line...")
            line = fp.readline()
            logger.debug(f"Line read: {line}")
            if not line:
                logger.debug("No line, Async sleeping for .1")
                await asyncio.sleep(1)
                continue
            elif not (matches := re.search(COMMAND_RE, line)):
                logger.debug("Bad line, continuing...")
                continue
            
            username = matches.group(1)
            service = matches.group(2)
            args = matches.group(3) or ""
            if service is None:
                logger.debug("Bad service, Async sleeping for .1")
                await asyncio.sleep(.1)
                continue
            
            logger.debug(f"Console log matched pattern: {username}, {service} {args}, putting to queue")
            await command_queue.put((username, service, *[a.strip() for a in args.split(" ")]))
            logger.debug("Queue put! Going again")
            last_size = fp.tell()

async def main():
    command_queue = asyncio.Queue()

    try:
        await asyncio.gather(
            poll_console_log(command_queue),
            command_dispatcher(command_queue),
            goblin_clicker.run(),
        )
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        logger.info("Done!")
    except Exception as err:
        logger.error(str(err), err.args)
        raise
    finally:
        goblin_clicker.save()

if __name__ == "__main__":
    asyncio.run(main())
    
