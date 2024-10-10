# Server code (server.py) for Asymmetric Ciphers - RSA, ElGamal, ECC
import socket
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ElGamal
from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64

# Helper functions for asymmetric ciphers
def rsa_encrypt(plaintext):
    key = RSA.generate(2048)
    public_key = key.publickey()
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()

def elgamal_encrypt(plaintext):
    key = ElGamal.generate(2048, get_random_bytes)
    public_key = key.publickey()
    plaintext_bytes = bytes_to_long(plaintext.encode())
    k = get_random_bytes(32)  # Random value for encryption
    ciphertext = public_key.encrypt(plaintext_bytes, k)
    return base64.b64encode(long_to_bytes(ciphertext[0]) + long_to_bytes(ciphertext[1])).decode()

def ecc_encrypt(plaintext):
    key = ECC.generate(curve='P-256')
    public_key = key.public_key()
    h = SHA256.new(plaintext.encode())
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    return base64.b64encode(signature).decode()

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Received: {request}")
    
    command, message = request.split('|')
    
    if command == "RSA":
        encrypted_message = rsa_encrypt(message)
    elif command == "ELGAMAL":
        encrypted_message = elgamal_encrypt(message)
    elif command == "ECC":
        encrypted_message = ecc_encrypt(message)
    else:
        encrypted_message = "Invalid command"

    client_socket.send(encrypted_message.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:9999")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[+] Accepted connection from {addr}")
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()