import logging

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class LocalDirectoryWatcher(object):
    def __init__(self, path: str):
        self.path = path
        self.observer = None  # type: Observer

    def start(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.join()
