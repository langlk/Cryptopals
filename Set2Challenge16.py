# Cryptopals
# Set 2 Challenge 16

import base64
from Crypto.Cipher import AES
from random import randint

# Decrypt with AES in ECB
def AES_ECB_decrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.decrypt(bytes_code)

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

# Encrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_encrypt(bytes_code, key, blocksize):
    encrypted_block = bytes([0]) * blocksize
    final_code = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        xORblock = binary_xOR(block, encrypted_block)
        encrypted_block = AES_ECB_encrypt(xORblock, key)
        final_code += encrypted_block
    return final_code

# Decrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_decrypt(bytes_code, key, blocksize):
    encrypted_block = bytes([0]) * blocksize
    final_message = b''
    for i in range(0, len(bytes_code), blocksize):
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

def random_bytes(n):
    random_ints = []
    for i in range(n):
        random_ints.append(randint(0,255))
    return bytes(random_ints)

RANDOM_KEY = random_bytes(16)
RANDOM_PADDING = random_bytes(randint(5,10))

def random_encode(message):
    message = pad_PKCS_7(RANDOM_PADDING + message, 16)
    return AES_ECB_encrypt(message, RANDOM_KEY)

def oracle_function(message):
    
