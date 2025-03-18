import socket
import pickle

class Bob:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.n = None  # Alice's public modulus
        self.e = None  # Alice's public exponent
    
    def start(self):
        """
        Start the client process
        """
        try:
            # First, receive the public key from Alice
            self.receive_public_key()
            
            # Then, encrypt and send a message to Alice
            self.encrypt_and_send_message()
            
        except Exception as e:
            print(f"Error: {e}")
    
    def receive_public_key(self):
        """
        Receive public key from Alice
        """
        try:
            print(f"Connecting to Alice at {self.host}:{self.port} to receive public key...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Connected to Alice for key exchange")
            
            # Receive data from the socket
            data = b""
            while True:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            
            # Unpickle the public key
            public_key = pickle.loads(data)
            self.n, self.e = public_key
            
            print("Received public key from Alice:")
            print(f"n: {self.n}")
            print(f"e: {self.e}")
            
            client_socket.close()
            
        except Exception as e:
            print(f"Error receiving public key: {e}")
    
    def encrypt_and_send_message(self):
        """
        Encrypt a message using Alice's public key and send it
        """
        try:
            # Get message from user
            message = input("Enter message to encrypt and send to Alice: ")
            
            # Convert message to integer
            message_bytes = message.encode('utf-8')
            plaintext = int.from_bytes(message_bytes, 'big')
            
            # Check if message is smaller than n
            if plaintext >= self.n:
                print("Message too large for the key size. Please use a shorter message.")
                return
            
            # Encrypt message using Alice's public key
            ciphertext = pow(plaintext, self.e, self.n)
            print(f"Encrypted message: {ciphertext}")
            
            # Send encrypted message to Alice
            print(f"Connecting to Alice at {self.host}:{self.port} to send encrypted message...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Connected to Alice for sending encrypted message")
            
            # Pickle and send the ciphertext
            data = pickle.dumps(ciphertext)
            client_socket.sendall(data)
            
            print("Encrypted message sent to Alice")
            client_socket.close()
            
        except Exception as e:
            print(f"Error encrypting and sending message: {e}")

if __name__ == "__main__":
    bob = Bob()
    bob.start()