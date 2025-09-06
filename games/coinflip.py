import random
import time
from utils import write_and_send_command, press_key

async def flip(username:str):
    time.sleep(0.5)
    random_num = random.randint(0,1)
    if(random_num == 0):
      await write_and_send_command(f"say {username} flipped heads! ⚫")
    else:
      await write_and_send_command(f"say {username} flipped tails! ⚪")