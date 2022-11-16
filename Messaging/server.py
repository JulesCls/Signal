from threading import Thread
import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)

print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

listOfClient = {}

def getNameFromMsg(msg):
    return msg.split(":")[0].split("] ")[1]

def listenForClient(cs):
    while True:
        try:
            msg = cs.recv(2048).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            listOfClient.pop(cs)
        else:
            msg = msg.replace(separator_token, ": ")
            name = (msg.split(":")[0].split("] "))[1]
            listOfClient[cs] = name

        for client_socket in listOfClient:
            client_socket.send(msg.encode())

def broadcast(msg):
    for client_socket in listOfClient:
        client_socket.send(msg.encode())

# def unicast(msg, clientSocket):


while True:
    cs, clientAddress = server.accept()
    print(f"{clientAddress} connected")

    t = Thread(target=listenForClient, args=(cs,))
    t.daemon = True
    t.start()

    print(listOfClient)

for cs in listOfClient:
    cs.close()
server.close()


