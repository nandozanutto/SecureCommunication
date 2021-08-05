#!/usr/bin/env python3
import DH
from simplecrypt import encrypt, decrypt

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

modulo = DH.random_with_N_digits(3)
b = DH.random_with_N_digits(5)
me = DH.Communicator(5, modulo, b)
partial = me.generatePartialKey()

# print("Partial of Client", partial)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(modulo.to_bytes(5, 'little'))
    data = s.recv(1024)
    partialR = int.from_bytes(data, "little")
    # print("partial of server ", partialR)
    s.sendall(partial.to_bytes(5, 'little'))
    # print("my partial", partial)

    fullKey = me.generateFullKey(partialR)
    inputMessage = input("Type message\n") 
    message = me.encrypt_message(inputMessage)
    s.sendall(message)

    data = s.recv(1024)
    messageR = me.decrypt_message(data)
    print("Answer from server\n->", messageR)

    # try:
    #     messageTest = decrypt("123", data)
    # except:
    #     print("Wrong Password!!")



