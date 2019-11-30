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
                    filename = conn.recv(1024).decode("utf-8")
                    length = filename.find("\n")

                    with open(filename[:length], 'wb') as file:
                        data = filename[length + 1:].encode('utf-8')
                        while data:
                            file.write(data)
                            data = conn.recv(1024)


ReceiverServer().serve()
