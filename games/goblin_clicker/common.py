import os
from datetime import timedelta

CURRENT_DIR = os.path.dirname(__file__)
RES_DIR = os.path.join(CURRENT_DIR, "res")
SAVE_INTERVAL = timedelta(seconds=180)

GROWTH_RATE: float = 1.2