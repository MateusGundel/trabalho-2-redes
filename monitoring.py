import logging
import threading
import time

import ping
from util import utils
from util.mail import Mail
from util.send_file import Messages


class MappingFiles:
    def __init__(self, path, user, server_ip):
        self.path = path
        self.messages = Messages()
        self.user = user
        self.server_ip = server_ip
        print("Starting")

    def map_and_send(self):
        file_structure = utils.files_to_dict(self.path)
        self.messages.send_message(file_structure, self.path, self.user)

    def mapping(self):
        time.sleep(10)
        self.map_and_send()

    def ping_to_server(self):
        error = False
        while True:
            try:
                result = ping.do_one(self.server_ip, 2)
                if not result:
                    if not error:
                        Mail().sendMail("PING - Servidor " + self.server_ip + "está com erro", "mateusgundel@gmail.com")
                        logging.error("PING - Servidor " + self.server_ip + "está com erro")
                        error = True
                else:
                    logging.info("PING - Server OK")
                    error = False
            except:
                if not error:
                    Mail().sendMail("PING -Servidor " + self.server_ip + "está com erro", "mateusgundel@gmail.com")
                    logging.error("PING - Servidor " + self.server_ip + "está com erro")
                    error = True
            time.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    try:
        # path a ser monitorado
        path = '/home/mateus.gundel/histograma'
        # pasta de usuário
        user = 'default'
        server_ip = 'google.com'

        mapper = MappingFiles(path, user, server_ip)

        mapp_thread = threading.Thread(target=mapper.mapping)
        ping_thread = threading.Thread(target=mapper.ping_to_server)
        mapp_thread.start()
        ping_thread.start()

    except KeyboardInterrupt:
        logging.error("Programa encerrado")
