# Client code (client.py) for Asymmetric Ciphers - RSA, ElGamal, ECC
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    
    # Get user input for command and message
    command = input("Enter command (RSA, ELGAMAL, ECC): ")
    message = input("Enter message to encrypt: ")
    
    # Send command and message to server
    client.send(f"{command}|{message}".encode())
    encrypted_message = client.recv(4096).decode()
    print(f"Encrypted message: {encrypted_message}")  # Encrypted message from server
    
    client.close()

if __name__ == "__main__":
    main()