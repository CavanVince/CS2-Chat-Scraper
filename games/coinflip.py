import random
import time
from utils import write_command, press_key

def flip(username:str):
    time.sleep(0.5)
    random_num = random.randint(0,1)
    if(random_num == 0):
        write_command(f"say {username} flipped heads! ⚫")
    else:
        write_command(f"say {username} flipped tails! ⚪")