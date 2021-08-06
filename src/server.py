#!/usr/bin/env python3
import DH

import socket
import logging as log

format = 'Server - %(levelname)s - %(message)s'
file = './../log/log.txt'
log.basicConfig(filename=file, format=format, level=log.INFO)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

print(f"Server is starting on {HOST} and port {PORT}")
log.info("Server is starting on %s and port %d", HOST, PORT)

b = DH.random_with_N_digits(5)
print("Generating a random number: ", b)
log.info("Generating a random number: %d", b)
ack = 1

print("Server - Initializing the socket connection")
log.info("Initializing the socket connection")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server - Waiting for a connection")
    log.info("Waiting for a connection")

    conn, addr = s.accept()
    with conn:
        print(f"Server - {addr} connected")
        log.info("%s connected", conn)
        while True:
            data = conn.recv(1024)
            print("Server - Waiting for client message")
            log.info("Waiting for client message")
            if not data:
                break#cliente cancelou conexao
            
                
            messageType = int.from_bytes(data, 'little')
            conn.sendall(ack.to_bytes(5, 'little'))
            print("Server - Receiving the message indicanting to server if is to use crypt or not")
            log.info("Receiving the message indicanting to server if is to use crypt or not")

            if(messageType == 0):
                data = conn.recv(1024)
                modulo = int.from_bytes(data, "little")#recebe o módulo recebido do cliente e transforma em int
                print("Server - Receiving the module from client")
                log.info("Receiving the module from client")

                me = DH.Communicator(5, modulo, b)
                partial = me.generatePartialKey()
                print("Server - Generating a partial key: ", partial)
                log.info("Generating a partial key: %s", partial)

                conn.sendall(partial.to_bytes(5, 'little'))
                print("Server - Sending the partial key to client")
                log.info("Sending the partial key to client")

                # print("my partial", partial)
                data = conn.recv(1024)
                partialR = int.from_bytes(data, "little")
                print("Receiving the client partial key: ", partialR)
                log.info("Receiving the client partial key: %s", partialR)

                # print('Partial Key Received', partialR)
                data = conn.recv(1024)
                print('Server - Message received', data)
                log.info("Message received")

                fullKey = me.generateFullKey(partialR)
                print("Server - Generating full key: ", fullKey)
                log.info("Generating full key: %s", fullKey)

                print("Decrypting the message: ", fullKey)
                log.info("Decrypting the message: %s", fullKey)

                messageR = me.decrypt_message(data)
                print("Server - Message decrypted: ", messageR)
                log.info("Message decrypted: %s", messageR)

                print("Server - Encrypting the message")
                log.info("Encrypting the message")
                message = me.encrypt_message(messageR)

                print("Server - Sending the encrypt message: ", message)
                log.info("Sending the encrypted message: %s", message)
                conn.sendall(message)

            else:
                data = conn.recv(1024)
                print('Server - Message received', data)
                log.info("Message received")
                conn.sendall(data)



