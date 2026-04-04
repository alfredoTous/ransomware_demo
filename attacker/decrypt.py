import socket

PORT = 1234

server = socket.socket()
server.bind(("127.0.0.1", PORT))
server.listen()
conn, addr = server.accept()
with open("secret.bin", "rb") as file:
    secret_key = file.read()

conn.sendall(secret_key)
