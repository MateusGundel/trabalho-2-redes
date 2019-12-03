import json
import logging
import os
import socket


class Messages:
    def __init__(self, host="localhost", port=2468):
        self.host = host
        self.port = port

    def send_message(self, data, path, user='default'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            # Manda a estrutura de pastas
            s.send(json.dumps({'data': data, 'user': user}).encode('utf-8'))

            # espera o server responder
            response = s.recv(1024).decode("utf-8")
            logging.info(response)
            # se a resposta for o nome de um arquivo, entra em um loop pq pode ser solicitado mais
            # se recebe ok os arquivos estão atualizados
            while response and 'ok' != response:
                try:
                    # carrega o arquivo pra memória
                    with open(os.path.join(path, response), "rb") as file:
                        # envia todos os bytes do arquivo
                        s.sendall(file.read())
                except:
                    logging.error("Error ao localizar o arquivo " + str(response))

                # espera para ver se vai requisitar mais arquivos
                response = s.recv(1024).decode("utf-8")
                logging.info("Recebeu -- " + response)

            logging.info("Encerrando conexão")
