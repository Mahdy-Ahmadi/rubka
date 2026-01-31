import threading
import time
from typing import Callable

class Job:
    def __init__(self, delay: int, callback: Callable):
        self.delay = delay
        self.callback = callback
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        time.sleep(self.delay)
        self.callback()
