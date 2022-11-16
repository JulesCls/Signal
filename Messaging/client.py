import socket
from threading import Thread
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = "<SEP>"

client = socket.socket()
print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}")
client.connect((SERVER_HOST, SERVER_PORT))
print("Connected")

name = input("Enter a pseudo: ")
client.send(name.encode())

def listenForMessages():
    while True:
        msg = client.recv(2048).decode()
        print("\n" + msg)

t =Thread(target=listenForMessages)
t.daemon = True
t.start()

while True:
    toSend = input()

    if toSend.lower() == "q":
        break
    dateNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    toSend = f"[{dateNow}] {name}: {toSend}"
    client.send(toSend.encode())

client.close()

