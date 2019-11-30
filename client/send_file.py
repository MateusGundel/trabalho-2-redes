import socket


class Sender:
    def __init__(self, host="localhost", port=7777):
        self.host = host
        self.port = port

    def send_file(self, filename):
        with socket.socket() as s:
            s.connect((self.host, self.port))

            s.send((filename+"\n").encode('utf-8'))
            with open(filename, "rb") as file:
                s.sendall(file.read())


Sender().send_file("teste.txt")
