# Cryptopals
# Set 3 Challenge 17

# CBC Padding Oracle

import base64
from Crypto.Cipher import AES
from random import randint

def random_bytes(n):
    random_ints = []
    for i in range(n):
        random_ints.append(randint(0,255))
    return bytes(random_ints)

def binary_xOR(byte_code1,byte_code2):
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

# Decrypt with AES in ECB
def AES_ECB_decrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.decrypt(bytes_code)

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

# Encrypt with CBC, IV = b'\x00'*blocksize
def CBC_encrypt(bytes_code, key, blocksize):
    initialization_vector = random_bytes(blocksize)
    encrypted_block = initialization_vector
    final_code = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        xORblock = binary_xOR(block, encrypted_block)
        encrypted_block = AES_ECB_encrypt(xORblock, key)
        final_code += encrypted_block
    return initialization_vector + final_code

# Decrypt with CBC, IV = b'\x00'*blocksize
def CBC_decrypt(bytes_code, key, blocksize):
    initialization_vector = bytes_code[:blocksize]
    encrypted_block = initialization_vector
    final_message = b''
    for i in range(blocksize, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        decrypted_block = AES_ECB_decrypt(block, key)
        xORblock = binary_xOR(decrypted_block, encrypted_block)
        final_message += xORblock
        encrypted_block = block
    return final_message

def pad_PKCS_7(message, blocksize):
    padding_amount = blocksize - len(message) % blocksize
    if padding_amount == 0:
        padding_amount = blocksize
    padding = bytes([padding_amount]) * padding_amount
    return message + padding

def is_PKCS_7(plainbytes):
    for byte in plainbytes[len(plainbytes) - plainbytes[-1]:]:
        if byte != plainbytes[-1]:
            return False
    return True

RANDOM_KEY = random_bytes(16)
POSSIBLE_MESSAGES = [b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=", b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=", b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==", b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==", b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl", b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==", b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==", b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=", b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=", b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
ACTUAL_MESSAGE = POSSIBLE_MESSAGES[randint(0, len(POSSIBLE_MESSAGES) - 1)]

def oracle_encrypt():
    return CBC_encrypt(pad_PKCS_7(ACTUAL_MESSAGE, 16), RANDOM_KEY, 16)

def padding_oracle(message):
    decrypted_message = CBC_decrypt(message, RANDOM_KEY, 16)
    return is_PKCS_7(decrypted_message)

test_message = oracle_encrypt()
print(CBC_decrypt(test_message, RANDOM_KEY, 16))
print(padding_oracle(test_message))
