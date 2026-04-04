
import os
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


PORT = 1234


def decrypt(data, key):
    iv = data[:16]
    ciphertext = data[16:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext


def get_secret_key():
    client = socket.socket()
    client.connect(("127.0.0.1", PORT))
    secret_key = client.recv(4096)
    return secret_key


def main():
    secret_key = get_secret_key()
    target_path = "./lab/sample_cipher"
    new_path = "./lab/sample_plain/"
    os.makedirs(new_path, exist_ok=True)
    for root, dirs, files in os.walk(target_path):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                data = f.read()
            plaintext_path = file_path[:len(file_path)-4]
            os.remove(file_path)
            plaintext = decrypt(data, secret_key)
            with open(plaintext_path, "w") as f:
                f.write(plaintext.decode())
    os.rename(target_path, new_path)
 

if __name__ == "__main__":
    main()

