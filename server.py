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
            # aceita até 10 conexões
            s.listen(10)

            while True:
                conn, addr = s.accept()
                with conn:
                    print("Connection from: " + str(addr))
                    full_data = json.loads(conn.recv(1024).decode("utf-8"))
                    # recebe um usuário e uma estrutura de pastas.
                    user = full_data['user']
                    self.user_path = self.base_path + '/' + user
                    data = full_data['data']

                    # cria pasta do usuário se não existir
                    if not os.path.exists(self.user_path):
                        os.makedirs(self.user_path)

                    # verifica se a estrutura de pastas do client é diferente do server
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
        # realiza o request de um arquivo para o client
        logging.info("Requesting - " + file)

        # manda para o client qual arquivo precisa
        conn.sendall(file.encode('utf-8'))

        # recebe os bytes do arquivo ou error
        data = conn.recv(1024)
        if data != 'error' or data:
            # cria o arquivo e persiste ele
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
        # itera sobre as pastas para ver se elas já existem no servidor
        for item in client_structure:
            # Se for um dict, é uma pasta e eu preciso entrar nela para verificar
            if isinstance(client_structure[item], dict):
                # se a pasta ainda não existir, cria ela
                if not os.path.exists(os.path.join(self.user_path, root, item)):
                    os.makedirs(os.path.join(self.user_path, root, item))
                # Entra nas pastas recursivamente
                self.find_wrong_files(conn, client_structure[item], os.path.join(root, item))
            # Se não é um dict, é um arquivo
            else:
                # se já existe o arquivo ou o tamanho do arquivo é diferente do enviado
                # requisita o arquivo ao client
                if (not os.path.exists(os.path.join(self.user_path, root, item)) or
                        os.path.getsize(os.path.join(self.user_path, root, item)) != client_structure[item]):
                    logging.info("Making request to file - " + root + "/" + item)
                    self.request_data(conn, os.path.join(root, item), client_structure[item])

    def find_excluded_files(self, client_structure, local_structure, root):
        # itera sobre a strutura de pastas
        for iten in local_structure:
            # verifica se tem os arquivos no client
            if iten not in client_structure:
                # se não tem no client, exclui o arquivo
                if os.path.isfile(os.path.join(self.user_path, root, iten)):
                    os.remove(os.path.join(self.user_path, root, iten))
                else:
                    shutil.rmtree(os.path.join(self.user_path, root, iten))
            else:
                # se for um dir, tem que verificar dentro das pastas
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
