from watchdog.observers import Observer

from watcher.local_directory_event_handler import LocalDirectoryEventHandler


class LocalDirectoryWatcher(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self.observer = None  # type: Observer

    def start(self):
        event_handler = LocalDirectoryEventHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()
