import logging
import os
from os import path

import time

from config.config import SecureCloudConfig
from watcher.local_directory_watcher import LocalDirectoryWatcher


class SecureCloud(object):
    def __init__(self) -> None:
        self.local_directory_watcher = None  # type: LocalDirectoryWatcher

    def check_directories(self) -> None:
        if not path.exists(SecureCloudConfig.local_directory):
            os.makedirs(SecureCloudConfig.local_directory)
        if not path.exists(SecureCloudConfig.temporary_directory):
            os.makedirs(SecureCloudConfig.temporary_directory)

    def start(self) -> None:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.check_directories()
        self.local_directory_watcher = LocalDirectoryWatcher(SecureCloudConfig.local_directory)
        self.local_directory_watcher.start()

    def stop(self) -> None:
        self.local_directory_watcher.stop()
        self.local_directory_watcher.join()

if __name__ == '__main__':
    secure_cloud = SecureCloud()
    secure_cloud.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        secure_cloud.stop()
