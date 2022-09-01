from typing import Callable, List
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import time
import numpy as np

from util.load_csv_with_mask import load_csv_with_mask

class CsvHandler(PatternMatchingEventHandler):
    """
    特定のcsvファイルを監視し、変更があった場合に内容をコールバックに流す
    """
    def __init__(
        self, 
        patterns: List[str], 
        dir: str,
        on_changed: Callable[[np.ndarray], None]):
        super(CsvHandler, self).__init__(patterns=patterns)
        self.dir = dir
        self.on_changed = on_changed
        self.observer = Observer()
        self.observer.schedule(self, self.dir, recursive=False)
        self.observer.start()
        self.previous_text = ""
        print("Started watching")
    def on_created(self, event):
        print("File created: ", event.src_path)
        new_text = self.load_text(event.src_path)
        if new_text != self.previous_text:
            self.on_changed(load_csv_with_mask(event.src_path))
            self.previous_text = new_text

    def on_modified(self, event):
        print("File modified: ", event.src_path)
        new_text = self.load_text(event.src_path)
        if new_text != self.previous_text:
            self.on_changed(load_csv_with_mask(event.src_path))
            self.previous_text = new_text

    def load_text(self, path):
        with open(path, "r") as f:
            return f.read()

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print("Stopped watching")

if __name__ == "__main__":
    target_dir = "."
    target_file = "watched.csv"
    csv_handler = CsvHandler([target_file], target_dir, lambda x: print(x))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        csv_handler.stop()
        print("Stopped")

    csv_handler.stop()
