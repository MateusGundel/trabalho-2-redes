import logging
import time

from util import utils
from util.send_file import Messages


class MappingFiles:
    def __init__(self, path, user):
        self.path = path
        self.messages = Messages()
        self.user = user
        print("Starting")

    def map_and_send(self):
        file_structure = utils.files_to_dict(self.path)
        self.messages.send_message(file_structure, self.path, self.user)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # path a ser monitorado
    path = '/home/mateus/update'
    # pasta de usuário
    user = 'default'
    mapper = MappingFiles(path, user)

    try:
        while True:
            time.sleep(10)
            mapper.map_and_send()

    except KeyboardInterrupt:
        logging.error("Programa encerrado")
