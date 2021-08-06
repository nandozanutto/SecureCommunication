#!/usr/bin/env python3
import DH
from simplecrypt import encrypt, decrypt
import socket
import logging as log

format = 'Client - %(levelname)s - %(message)s'
file = './../log/log.txt'
log.basicConfig(filename=file, format=format, level=log.INFO)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

print(f"Server is starting on {HOST} and port {PORT}")
log.info("Server is starting on %s and port %d", HOST, PORT)

modulo = DH.random_with_N_digits(3)#definindo aleatoriamente o valor que será usado para fazer o módulo
print(f"Client - Definig the module: {modulo}")
log.info("Defining the module of the client: %d", modulo)

b = DH.random_with_N_digits(5)#definindo a chave privada
print(f"Client - Defining the secret key: {b}")
log.info("Defining the secret key: %d", b)

me = DH.Communicator(5, modulo, b)#criando o objeto comunicador
partial = me.generatePartialKey()#cria-se a chave parcial
print(f"Client - Defining the partial key: {partial}")
log.info("Defining the partial key: %d", partial)

messageType = int(input("Digit the type of communication: \n0: With cryptography\n1: Without cryptography\n"))#0: comunicação criptografada 1: comunicação normal 2: teste
if(messageType == 0):
    log.info("Communcation with cryptography")
else:
    log.info("Communcation without cryptography")


print("Client - Initializing the socket connection")
log.info("Initializing the socket connection")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # Send to server the message saying if the communication is with cript or not 
    s.sendall(messageType.to_bytes(5, 'little'))
    data = s.recv(1024)#recebendo ack
    
    if(messageType == 0):
        s.sendall(modulo.to_bytes(5, 'little'))#to_bytes pois o socket envia em bytes object
        print(f"Client - Sending the module to server: {modulo}")
        log.info("Sending the module to server")

        data = s.recv(1024)#recebendo dados
        partialR = int.from_bytes(data, "little")#chave parcial estrangeira é recebida
        print(f"Client - Receiving the server partial key: {partialR}")
        log.info("Receiving the server partial key: %s", partialR)

        # print("partial of server ", partialR)
        s.sendall(partial.to_bytes(5, 'little'))#envia a chave parcial do client
        print(f"Client - Sending the partial key to server: {partial}")
        log.info("Sending the partial key to server: %s", partial)
        # print("my partial", partial)
        fullKey = me.generateFullKey(partialR)#cria chave inteira
        print(f"Client - Creating the full key: {fullKey}")
        log.info("Creating the full key: %s", fullKey)
    
        inputMessage = input("Type a message\n")#pede mensagem ao usuário
        log.info("Sending a menssagem to server: %s", inputMessage)

        message = me.encrypt_message(inputMessage)
        print(f"Client - Encrypting the message and sending to server: {message}")
        log.info("Encrypting the message and sending to server: %s", message)
        s.sendall(message)

        data = s.recv(1024)
        messageR = me.decrypt_message(data)
        print(f"Client - Decrypt the answer from the server: {messageR}")
        log.info("Decrypt the answer from the server: %s", messageR)

        print("Answer from server\n->", messageR)

        print("Would you like to test for worng passwords ? ")
        test = int(input("Y: 1 | N: 0\n"))
        if test == 1:
            print("Testing wrong passwords")
            for i in range(3):
                try:
                    messageTest = decrypt(DH.random_with_N_digits(3), data)
                    print(f"Testing for wrong password: {messageTest}")
                    log.info("Testing for wrong password: %s", messageTest)
                except:
                    print("Wrong Password!!")



    else:
        inputMessage = input("Type message\n")#pede mensagem ao usuário
        print("Seding a message without criptography")
        log.info("Sending a message without criptography")
        arr = bytes(inputMessage, 'utf-8')
        s.sendall(arr)
        data = s.recv(1024)
        print("Answer from server\n->", data)

    

    




