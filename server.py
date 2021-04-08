import socket
from _thread import *
import pickle
from board import Board

IP = "localhost"
PORT = 50000

#List of connected clients:
clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen()
first = True
board = Board()
board.init_game()

print('Server started, waiting for connections')

def threaded_client(conn):
    global first
    conn.send(str(first).encode('utf-8'))
    first = False
    while True:
        try:
            data = conn.recv(2048)
            '''
            if not data:
                print("Disconnected")
                break
            '''
            if data:
                print(data)
                msg = pickle.loads(data)
                print('received: ',msg)

                for client in clients:
                    if client != conn:
                        client.send(data)
        except Exception as e:
            print(e)
            break
    
    print("connection lost")
    clients.remove(client)
    conn.close()

while True:
    conn, adress = server_socket.accept()
    print('Connected to ', adress)

    if conn not in clients and len(clients) < 2:
        start_new_thread(threaded_client, (conn,))
        clients.append(conn)


