import logging
import time

from send_file import Sender
from watchdog.events import DirModifiedEvent
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

user = "mateus"


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        global user
        self.sender = Sender()
        self.user = user

    def on_any_event(self, event):
        logging.info("any =============")
        list_pass = ['.swp', '/.', '.swx']
        if DirModifiedEvent is not type(event) and not any(x in event.src_path for x in list_pass):
            logging.info(event)
    # def on_created(self, event):
    #     logging.info("created =============")
    #     if(event.event_type)
    #     logging.info(event)
    #     # self.sender.send_file(event.src_path, self.user)
    #
    # def on_moved(self, event):
    #     logging.info("moved =============")
    #     logging.info(event)
    #
    # def on_modified(self, event):
    #     logging.info("modified =============")
    #     logging.info(event)
    #
    # def on_deleted(self, event):
    #     logging.info("deleted =============")
    #     logging.info(event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '/home/mateus/update'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
