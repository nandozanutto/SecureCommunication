#!/usr/bin/env python3
import DH

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

b = DH.random_with_N_digits(5)

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
            
            modulo = int.from_bytes(data, "little")#recebe o módulo recebido do cliente e transforma em int
            me = DH.Communicator(5, modulo, b)
            partial = me.generatePartialKey()
            conn.sendall(partial.to_bytes(5, 'little'))
            # print("my partial", partial)
            data = conn.recv(1024)
            partialR = int.from_bytes(data, "little")
            # print('Partial Key Received', partialR)

            data = conn.recv(1024)
            print('Message Received\n->', data)
            fullKey = me.generateFullKey(partialR)
            messageR = me.decrypt_message(data)
            print("Decrypted\n-> ", messageR)

            message = me.encrypt_message(messageR)
            conn.sendall(message)





