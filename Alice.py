import socket
import pickle
import random
from math import gcd

class Alice:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = None
        self.d = None
        self.generate_rsa_keys()
        
    def is_prime(self, n, k=50):
        """
        Miller-Rabin primality test
        """
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
            
        # Find r and s such that n - 1 = 2^r * s where s is odd
        s, r = 0, n - 1
        while r % 2 == 0:
            s += 1
            r //= 2
            
        # Perform k tests
        for _ in range(k):
            a = random.randint(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                for _ in range(s - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
        return True
        
    def generate_large_prime(self, bit_length=512):
        """
        Generate a large prime number with given bit length
        """
        while True:
            # Generate a random odd number of bit_length bits
            p = random.getrandbits(bit_length)
            p |= (1 << bit_length - 1) | 1  # Ensure the number has exactly bit_length bits and is odd
            if self.is_prime(p):
                return p
    
    def generate_rsa_keys(self):
        """
        Generate RSA key pair with 1024-bit modulus
        """
        print("Generating p...")
        self.p = self.generate_large_prime(512)
        
        print("Generating q...")
        self.q = self.generate_large_prime(512)
        
        # Calculate n = p * q
        self.n = self.p * self.q
        
        # Calculate φ(n) = (p-1) * (q-1)
        self.phi = (self.p - 1) * (self.q - 1)
        
        # Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
        self.e = 65537  # Common value for e
        
        # Check if e and phi are coprime
        if gcd(self.e, self.phi) != 1:
            raise ValueError("e and phi are not coprime")
        
        # Calculate d such that (d * e) % φ(n) = 1
        self.d = pow(self.e, -1, self.phi)
        
        print("RSA Keys generated successfully:")
        print(f"Public Key (n, e): ({self.n}, {self.e})")
        print(f"Private Key (d): {self.d}")
    
    def start_server(self):
        """
        Start TCP server to exchange keys and receive encrypted messages
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Alice is running on {self.host}:{self.port}")
            
            # First, send public key to Bob
            self.send_public_key(server_socket)
            
            # Then, receive encrypted message from Bob
            self.receive_and_decrypt(server_socket)
            
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()
    
    def send_public_key(self, server_socket):
        """
        Send public key (n, e) to Bob
        """
        try:
            print("Waiting for Bob to connect for key exchange...")
            client_socket, addr = server_socket.accept()
            print(f"Connected to Bob at {addr} for key exchange")
            
            # Send n and e as the public key
            public_key = (self.n, self.e)
            data = pickle.dumps(public_key)
            client_socket.sendall(data)
            
            print("Public key sent to Bob")
            client_socket.close()
            
        except Exception as e:
            print(f"Error sending public key: {e}")
    
    def receive_and_decrypt(self, server_socket):
        """
        Receive encrypted message from Bob and decrypt it
        """
        try:
            print("Waiting for Bob to send encrypted message...")
            client_socket, addr = server_socket.accept()
            print(f"Connected to Bob at {addr} for receiving encrypted message")
            
            # Receive data from the socket
            data = b""
            while True:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            
            # Unpickle the ciphertext
            ciphertext = pickle.loads(data)
            print(f"Received ciphertext: {ciphertext}")
            
            # Decrypt ciphertext using private key d
            plaintext_int = pow(ciphertext, self.d, self.n)
            
            # Convert plaintext integer to bytes and then to string
            plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
            message = plaintext_bytes.decode('utf-8')
            
            print(f"Decrypted message: {message}")
            client_socket.close()
            
        except Exception as e:
            print(f"Error receiving encrypted message: {e}")

if __name__ == "__main__":
    alice = Alice()
    alice.start_server()