#!/usr/bin/env python3
import DH

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

b = DH.random_with_N_digits(5)
me = DH.Communicator(5, 129, b)
partial = me.generatePartialKey()
print("Partial of Server", partial)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break#cliente cancelou conexao
            partialR = int.from_bytes(data, "little")
            print('Partial Key Received', partialR)
            conn.sendall(partial.to_bytes(5, 'little'))
            data = conn.recv(1024)
            print('Message Received', data)
            fullKey = me.generateFullKey(partialR)
            messageR = me.decrypt_message(data)
            print("Tradução:", messageR)



