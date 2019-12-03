import json
import logging
import os
import shutil
import socket

from util import utils


class ReceiverServer:
    def __init__(self, host="localhost", port=7777):
        self.host = host
        self.port = port
        self.base_path = 'backup'
        self.user_path = 'default'

    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            print("server Started")
            s.listen(10)

            while True:
                conn, addr = s.accept()
                with conn:
                    print("Connection from: " + str(addr))
                    full_data = json.loads(conn.recv(1024).decode("utf-8"))
                    user = full_data['user']
                    self.user_path = self.base_path + '/' + user
                    data = full_data['data']

                    if not os.path.exists(self.user_path):
                        os.makedirs(self.user_path)

                    if data != utils.files_to_dict(self.user_path):
                        logging.info("arquivos diferentes, sincronizando")
                        logging.info(data)
                        local_structure = utils.files_to_dict(self.user_path)
                        logging.info(local_structure)
                        self.find_excluded_files(data, local_structure, '')
                        self.find_wrong_files(conn, data, '')
                        logging.info("sync ended")
                    else:
                        logging.info("arquivos iguais, aguardando próximo sincronismo")
                    conn.sendall("ok".encode('utf-8'))

    def request_data(self, conn, file, file_size):
        logging.info("Requesting - " + file)
        conn.sendall(file.encode('utf-8'))

        data = conn.recv(1024)
        if data != 'error' or data:
            with open(os.path.join(self.user_path, file), 'wb') as f:
                data_size = 0
                while data:
                    f.write(data)
                    data_size += data.__sizeof__()
                    # Verificação para não ficar esperando mais dados após receber tudo
                    if data_size >= file_size:
                        break
                    data = conn.recv(1024)

    def find_wrong_files(self, conn, client_structure, root):
        for item in client_structure:
            if isinstance(client_structure[item], dict):
                if not os.path.exists(os.path.join(self.user_path, root, item)):
                    os.makedirs(os.path.join(self.user_path, root, item))
                self.find_wrong_files(conn, client_structure[item], os.path.join(root, item))
            else:
                if (not os.path.exists(os.path.join(self.user_path, root, item)) or
                        os.path.getsize(os.path.join(self.user_path, root, item)) != client_structure[item]):
                    logging.info("Making request to file - " + root + "/" + item)
                    self.request_data(conn, os.path.join(root, item), client_structure[item])

    def find_excluded_files(self, client_structure, local_structure, root):
        for iten in local_structure:
            if iten not in client_structure:
                if os.path.isfile(os.path.join(self.user_path, root, iten)):
                    os.remove(os.path.join(self.user_path, root, iten))
                else:
                    shutil.rmtree(os.path.join(self.user_path, root, iten))
            else:
                if os.path.isdir(os.path.join(self.user_path, root, iten)):
                    self.find_excluded_files(client_structure[iten], local_structure[iten], os.path.join(root, iten))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    try:
        ReceiverServer().serve()
    except KeyboardInterrupt:
        logging.error("Servidor encerrado")
