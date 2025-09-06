import os
from datetime import timedelta

CURRENT_DIR = os.path.dirname(__file__)
SAVE_FILE_DIR = os.path.join(CURRENT_DIR, "res")
SAVE_INTERVAL = timedelta(seconds=180)

GROWTH_RATE: float = 1.07
ALHPA = 0.6