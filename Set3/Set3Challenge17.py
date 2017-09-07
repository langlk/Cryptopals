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
    if len(plainbytes) >= plainbytes[-1] and plainbytes[-1] != 0:
        for byte in plainbytes[len(plainbytes) - plainbytes[-1]:]:
            if byte != plainbytes[-1]:
                return False
        return True
    else:
        return False

RANDOM_KEY = random_bytes(16)
POSSIBLE_MESSAGES = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=", "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=", "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==", "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==", "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl", "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==", "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==", "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=", "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=", "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
ACTUAL_MESSAGE = base64.b64decode(POSSIBLE_MESSAGES[randint(0, len(POSSIBLE_MESSAGES) - 1)])

def oracle_encrypt():
    return CBC_encrypt(pad_PKCS_7(ACTUAL_MESSAGE, 16), RANDOM_KEY, 16)

def padding_oracle(message):
    decrypted_message = CBC_decrypt(message, RANDOM_KEY, 16)
    return is_PKCS_7(decrypted_message)

ciphertext = oracle_encrypt()


message_bytes = b""
ciphertext_copy = ciphertext
# loop for each 16-byte block
while len(ciphertext_copy) >= 32:
    # loop for each byte of block
    for j in range(1, 17):
        # loop for each possible character
        for i in range(256):
            if i != j or (len(ciphertext_copy) == len(ciphertext) and len(message_bytes) > 0 and j == message_bytes[-1]):
                test_block = binary_xOR(ciphertext_copy[-(16 + j):-(16)], bytes([i]) + message_bytes)
                test_block = binary_xOR(test_block, bytes([j]) * j)
                test_ciphertext = ciphertext_copy[:-(16 + j)] + test_block + ciphertext_copy[-16:]
                if (padding_oracle(test_ciphertext)):
                    message_bytes = bytes([i]) + message_bytes
                    break
    ciphertext_copy = ciphertext_copy[:-16]

if message_bytes == CBC_decrypt(ciphertext, RANDOM_KEY, 16):
    print("Correct!")
else:
    print("Nope!")
print("Found:", message_bytes, len(message_bytes))
print("Answer:", CBC_decrypt(ciphertext, RANDOM_KEY, 16),len(CBC_decrypt(ciphertext, RANDOM_KEY, 16)))
print("Original:", ACTUAL_MESSAGE)
