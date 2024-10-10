# Client code (client.py)
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    
    # Get user input for command and message
    command = input("Enter command (CAESAR, PLAYFAIR, HILL, VIGENERE, RAILFENCE, ROWTRANSPOSITION): ")
    message = input("Enter message to encrypt: ")
    
    # Send command to server
    client.send(command.encode())
    response = client.recv(1024).decode()
    print(response)  # Prompt from server for message
    
    # Send message to server
    client.send(message.encode())
    encrypted_message = client.recv(1024).decode()
    print(encrypted_message)  # Encrypted message from server
    
    client.close()

if __name__ == "__main__":
    main()