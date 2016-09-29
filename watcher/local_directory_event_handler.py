import os
import shutil
from os import path
from typing import Union

from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent, DirDeletedEvent, \
    FileDeletedEvent, \
    DirModifiedEvent, FileModifiedEvent, DirMovedEvent, FileMovedEvent

from config.config import SecureCloudConfig


class LocalDirectoryEventHandler(FileSystemEventHandler):
    @staticmethod
    def get_path_relative_to_local_directory(file_path: str) -> str:
        return file_path.replace(path.commonprefix([SecureCloudConfig.local_directory, file_path]), "").lstrip('/\\')

    @staticmethod
    def get_mapped_location(file_path: str) -> str:
        return path.join(SecureCloudConfig.temporary_directory,
                         LocalDirectoryEventHandler.get_path_relative_to_local_directory(file_path))

    def on_moved(self, event: Union[DirMovedEvent, FileMovedEvent]):
        """Called when a file or a directory is moved or renamed.

        :param event:
            Event representing file/directory movement.
        :type event:
            :class:`DirMovedEvent` or :class:`FileMovedEvent`
        """
        print("Move from", event.src_path, "=>", self.get_mapped_location(event.src_path))
        print("Move to  ", event.dest_path, "=>", self.get_mapped_location(event.dest_path))
        shutil.move(self.get_mapped_location(event.src_path), self.get_mapped_location(event.dest_path))

    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        """Called when a file or directory is created.

        :param event:
            Event representing file/directory creation.
        :type event:
            :class:`DirCreatedEvent` or :class:`FileCreatedEvent`
        """
        print("Create", event.src_path, "=>", self.get_mapped_location(event.src_path))
        if event.is_directory:
            os.mkdir(self.get_mapped_location(event.src_path))
        else:
            shutil.copy(event.src_path, self.get_mapped_location(event.src_path))

    def on_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]):
        """Called when a file or directory is deleted.

        :param event:
            Event representing file/directory deletion.
        :type event:
            :class:`DirDeletedEvent` or :class:`FileDeletedEvent`
        """
        print("Delete", event.src_path, "=>", self.get_mapped_location(event.src_path))
        if event.is_directory:
            shutil.rmtree(self.get_mapped_location(event.src_path))
        else:
            os.remove(self.get_mapped_location(event.src_path))

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]):
        """Called when a file or directory is modified.

        :param event:
            Event representing file/directory modification.
        :type event:
            :class:`DirModifiedEvent` or :class:`FileModifiedEvent`
        """
        print("Update", event.src_path, "=>", self.get_mapped_location(event.src_path))
        shutil.copy(event.src_path, self.get_mapped_location(event.src_path))
