#!/usr/bin/env python3

from random import randint
from simplecrypt import encrypt, decrypt

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class Communicator(object):
    def __init__(self, base, module, privateKey):
        self.base = base
        self.module = module
        self.privateKey = privateKey
        self.fullKey = None
        
    def generatePartialKey(self):
        partialKey = self.base**self.privateKey
        partialKey = partialKey%self.module
        return partialKey
    
    def generateFullKey(self, partialKeyR):
        fullKey = partialKeyR**self.privateKey
        fullKey = fullKey%self.module
        self.fullKey = fullKey
        return fullKey
    
    def encrypt_message(self, message):
        key = self.fullKey
        ciphercode = encrypt(str(key), message)
        return ciphercode
    
    def decrypt_message(self, encrypted_message):
        key = self.fullKey
        original = decrypt(str(key), encrypted_message).decode('utf8')
        return original



