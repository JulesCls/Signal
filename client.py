import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = "<SEP>"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client.connect((SERVER_HOST, SERVER_PORT))
    print('connected')
except:
    print('failed to connect')
finally:
    client.close()