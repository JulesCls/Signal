from threading import Thread
import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((SERVER_HOST, SERVER_PORT))
print("Listening on " + SERVER_HOST + ":" + str(SERVER_PORT))

while True:
    socket_server.listen()
    conn, addr = socket_server.accept()
    print('')


socket_server.close()
conn.close()



