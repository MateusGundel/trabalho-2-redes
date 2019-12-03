import json
import logging
import os
import socket


class Messages:
    def __init__(self, host="localhost", port=7777):
        self.host = host
        self.port = port

    def send_message(self, data, path, user='default'):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            s.send(json.dumps({'data': data, 'user': user}).encode('utf-8'))

            response = s.recv(1024).decode("utf-8")
            logging.info(response)
            while response and 'ok' != response:
                try:
                    with open(os.path.join(path, response), "rb") as file:
                        s.sendall(file.read())
                except:
                    logging.error("Error ao localizar o arquivo " + str(response))
                response = s.recv(1024).decode("utf-8")
                logging.info(response)
# Massages().send_file("{1:2}", 'gundel')
