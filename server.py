# Server code (server.py)
import socket
import numpy as np
import string

# Helper functions for ciphers
def caesar_cipher_encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            ciphertext += chr((ord(char) + key - shift) % 26 + shift)
        else:
            ciphertext += char
    return ciphertext

def playfair_cipher_encrypt(plaintext, key):
    # Implementation of Playfair cipher encryption
    # For simplicity, assume key is a 5x5 matrix of letters without 'J'
    matrix = create_playfair_matrix(key)
    plaintext_pairs = create_playfair_pairs(plaintext)
    ciphertext = ""
    for a, b in plaintext_pairs:
        a_row, a_col = find_position(matrix, a)
        b_row, b_col = find_position(matrix, b)
        if a_row == b_row:
            ciphertext += matrix[a_row][(a_col + 1) % 5] + matrix[b_row][(b_col + 1) % 5]
        elif a_col == b_col:
            ciphertext += matrix[(a_row + 1) % 5][a_col] + matrix[(b_row + 1) % 5][b_col]
        else:
            ciphertext += matrix[a_row][b_col] + matrix[b_row][a_col]
    return ciphertext

def create_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace('J', 'I') + string.ascii_uppercase.replace('J', '')))
    matrix = [list(key[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def create_playfair_pairs(plaintext):
    plaintext = plaintext.upper().replace('J', 'I')
    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    return pairs

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None

def hill_cipher_encrypt(plaintext, key_matrix):
    # Convert plaintext into vector form
    plaintext = plaintext.upper().replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += 'X'
    plaintext_vector = [ord(char) - 65 for char in plaintext]
    
    # Encryption
    ciphertext = ""
    for i in range(0, len(plaintext_vector), 2):
        vector = np.array(plaintext_vector[i:i+2]).reshape(2, 1)
        encrypted_vector = np.dot(key_matrix, vector) % 26
        ciphertext += chr(encrypted_vector[0][0] + 65) + chr(encrypted_vector[1][0] + 65)
    return ciphertext

def vigenere_cipher_encrypt(plaintext, key):
    key = key.upper()
    ciphertext = ""
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            key_char = key[i % key_length]
            key_shift = ord(key_char) - 65
            ciphertext += chr((ord(char) + key_shift - shift) % 26 + shift)
        else:
            ciphertext += char
    return ciphertext

def rail_fence_cipher_encrypt(plaintext, num_rails):
    rail = [[] for _ in range(num_rails)]
    direction_down = False
    row, col = 0, 0
    
    for char in plaintext:
        rail[row].append(char)
        if row == 0 or row == num_rails - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    
    ciphertext = ""
    for r in rail:
        ciphertext += "".join(r)
    return ciphertext

def row_transposition_cipher_encrypt(plaintext, key):
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    key_indices = [i for i, _ in key_order]
    num_cols = len(key)
    num_rows = len(plaintext) // num_cols + (len(plaintext) % num_cols != 0)
    
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    for i, char in enumerate(plaintext):
        grid[i // num_cols][i % num_cols] = char
    
    ciphertext = ""
    for col_index in key_indices:
        for row in grid:
            if row[col_index]:
                ciphertext += row[col_index]
    return ciphertext

def handle_client_connection(client_socket):
    client_socket.send(b"Enter command (CAESAR, PLAYFAIR, HILL, VIGENERE, RAILFENCE, ROWTRANSPOSITION): ")
    command = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Enter message to encrypt: ")
    message = client_socket.recv(1024).decode().strip()
    
    if command == "CAESAR":
        encrypted_message = caesar_cipher_encrypt(message, 3)  # Example key for Caesar Cipher
    elif command == "PLAYFAIR":
        encrypted_message = playfair_cipher_encrypt(message, "KEYWORD")  # Example key for Playfair Cipher
    elif command == "HILL":
        key_matrix = np.array([[3, 3], [2, 5]])  # Example key matrix for Hill Cipher
        encrypted_message = hill_cipher_encrypt(message, key_matrix)
    elif command == "VIGENERE":
        encrypted_message = vigenere_cipher_encrypt(message, "KEYWORD")  # Example key for Vigenere Cipher
    elif command == "RAILFENCE":
        encrypted_message = rail_fence_cipher_encrypt(message, 3)  # Example number of rails for Rail Fence Cipher
    elif command == "ROWTRANSPOSITION":
        encrypted_message = row_transposition_cipher_encrypt(message, "4312")  # Example key for Row Transposition Cipher
    else:
        encrypted_message = "Invalid command"

    client_socket.send(f"Encrypted message: {encrypted_message}".encode())
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