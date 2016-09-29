import os
from os import path

import time

from config.config import SecureCloudConfig
from watcher.local_directory_watcher import LocalDirectoryWatcher


class SecureCloud(object):
    def __init__(self):
        self.local_directory_watcher = None  # type: LocalDirectoryWatcher
        self.config = None  # type: SecureCloudConfig

    def start(self):
        self.config = SecureCloudConfig()
        if not path.exists(self.config.local_directory):
            os.makedirs(self.config.local_directory)
        self.local_directory_watcher = LocalDirectoryWatcher(self.config.local_directory)
        self.local_directory_watcher.start()

    def stop(self):
        self.local_directory_watcher.stop()


if __name__ == '__main__':
    secure_cloud = SecureCloud()
    secure_cloud.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        secure_cloud.stop()
    secure_cloud.local_directory_watcher.join()
