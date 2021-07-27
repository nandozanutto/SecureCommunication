#!/usr/bin/env python3
import DH

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


b = DH.random_with_N_digits(5)
me = DH.Communicator(5, 129, b)
partial = me.generatePartialKey()

print("Partial of Client", partial)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(partial.to_bytes(5, 'little'))
    data = s.recv(1024)

    partialR = int.from_bytes(data, "little")
    print('Received', partialR)#partialR: partialKey Received

    fullKey = me.generateFullKey(partialR)
    message = me.encrypt_message("hello from client")

    s.sendall(message)


