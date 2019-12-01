import os
import socket


class ReceiverServer:
    def __init__(self, host="localhost", port=7777):
        self.host = host
        self.port = port

    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            print("server Started")
            s.listen(10)

            while True:
                conn, addr = s.accept()
                with conn:
                    print("Connection from: " + str(addr))
                    full_data = conn.recv(1024).decode("utf-8")

                    #Pega o usuário de origem do arquivo.
                    length = full_data.find("\n")
                    user = full_data[:length]

                    #Pega o nome do arquivo.
                    filename = full_data[length + 1:]
                    length = filename.find("\n")

                    save_path = "backup/" + user
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    with open((save_path + "/" + filename[:length]), 'wb') as file:
                        data = filename[length + 1:].encode('utf-8')
                        while data:
                            file.write(data)
                            data = conn.recv(1024)







ReceiverServer().serve()
