import socket
import pickle

class Network:
    def __init__(self, IP, PORT):
        print(IP, PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP
        self.port = PORT
        self.addr = (self.server, self.port)
        self.id = self.connect() #Server sending back our id
        if self.id == "True":
            print("color: white")
        else:
            print("color: black")

    def connect(self):
        try:
            self.socket.connect(self.addr)
            print('Connected to the server')
            return self.socket.recv(1024).decode()
        except:
            pass
    
    def send(self,data):
        try:
            print(data)
            self.socket.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def wait_for_data(self):
        while True:
            data = self.socket.recv(1024)
            if data:
                return pickle.loads(data)