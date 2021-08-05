#!/usr/bin/env python3
import DH
import sys
from simplecrypt import encrypt, decrypt

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

modulo = DH.random_with_N_digits(3)#definindo aleatoriamente o valor que será usado para fazer o módulo
b = DH.random_with_N_digits(5)#definindo a chave privada
me = DH.Communicator(5, modulo, b)#criando o objeto comunicador
partial = me.generatePartialKey()#cria-se a chave parcial

# print("Partial of Client", partial)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    s.sendall(modulo.to_bytes(5, 'little'))#to_bytes pois o socket envia em bytes object
    data = s.recv(1024)#recebendo dados
    partialR = int.from_bytes(data, "little")#chave parcial estrangeira é recebida
    # print("partial of server ", partialR)
    s.sendall(partial.to_bytes(5, 'little'))#envia a chave parcial do client
    # print("my partial", partial)

    fullKey = me.generateFullKey(partialR)#cria chave inteira
    inputMessage = input("Type message\n")#pede mensagem ao usuário
    message = me.encrypt_message(inputMessage)
    s.sendall(message)

    data = s.recv(1024)
    messageR = me.decrypt_message(data)
    print("Answer from server\n->", messageR)

    with open('output.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(hex(id(s)))
    
    
    # try:
    #     messageTest = decrypt("123", data)
    # except:
    #     print("Wrong Password!!")



