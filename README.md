# RSA Implementation over TCP

This project implements the RSA encryption algorithm with a 1024-bit key size over TCP/IP sockets using Python

## Description

The implementation consists of two applications:

1. Alice: Generates RSA key pair and acts as a server
   - Generates two 512-bit prime numbers (p and q)
   - Calculates public key (n, e) and private key (d)
   - Sends public key to Bob
   - Decrypts messages from Bob

2. Bob: Client application that communicates with Alice
   - Receives Alice's public key
   - Encrypts user messages
   - Sends encrypted messages to Alice

## Implementation Details

- RSA Key Size: 1024 bits (two 512-bit primes)
- Encryption: C = M^e mod n
- Decryption: M = C^d mod n
- Communication: TCP sockets

## Requirements

- Python 
- Standard libraries: socket, pickle, random, math

## How to Run

1. Start Alice (server) in one terminal:
2.While running Alice's file, it will reach a point where it waits for Bob to connect. Once Alice is ready, you can run Bob's file in another terminal. Bob's file will prompt you to enter a message for encryption, which will be sent to Alice. Both terminals will display updates on the encryption and decryption process.