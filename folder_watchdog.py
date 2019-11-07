# -*- coding: utf-8 -*-

"""folder_watchdog.py
Demo of a folder watcher.
"""

from time import sleep
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchdogHandlerAny(FileSystemEventHandler):
    def __init__(self, watch_path):
        self.watch_path = watch_path

    def on_any_event(self, event):
        """Will be triggered if anything happen in the folder we're watching."""
        print("Something happened!")
        print(f"Event type: {event.event_type}")
        print(event)


class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, watch_path):
        self.watch_path = watch_path

    def on_modified(self, event):
        """Triggered when something is modified."""
        print(f"File modified: {event.src_path}")

    def on_created(self, event):
        """Triggered when a file or folder is created."""
        print(f"File created: {event.src_path}")

    def on_deleted(self, event):
        """Triggered when a file or folder is removed."""
        print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        """Triggered when a file or folder is moved.
        Note: Renaming is considered moving. Will only be considered moving if it's between watched folders."""
        print(f"{'Folder' if event.is_directory else 'File'} {event.event_type} "
              f"from: {path.relpath(event.src_path, self.watch_path)} "
              f"to: {path.relpath(event.dest_path, self.watch_path)}")


class FolderWatchDog:
    def __init__(self, handler):
        """
        Constructor
        :param handler: Who will handle what happens in our watch_path.
        """
        self.handler = handler
        self.watch_path = handler.watch_path
        self.observer = Observer()  # This is the class that does the actual watching.

    def start(self):
        self.observer.schedule(self.handler,
                               path=self.handler.watch_path,
                               recursive=True)  # If set to true, will watch every folder recursively.

        try:
            print(f"Starting to watch folder: {self.handler.watch_path}")
            self.observer.start()
            while True:
                sleep(5)

        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"Something went wrong...")
            print(e)

        finally:
            print("All done!")

    def stop(self):
        self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    to_watch = "/path/to/watch"
    w_dog = FolderWatchDog(handler=WatchdogHandlerAny(watch_path=to_watch))
    w_dog.start()
