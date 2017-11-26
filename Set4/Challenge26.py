# Cryptopals
# Set 4 Challenge 26

# CTR Bitflipping

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

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

def CTR_mode(key, nonce, blocksize, message):
    ciphertext = b''
    counter = 0
    while len(ciphertext) < len(message):
        key_stream = AES_ECB_encrypt(nonce + (counter).to_bytes(8, byteorder="little"), key)
        block = message[blocksize * counter:blocksize * counter + blocksize]
        ciphertext += binary_xOR(key_stream[:len(block)], block)
        counter += 1
    return ciphertext

def quote_illegal_chars(string):
    string = "\';\'".join(string.split(";"))
    string = "\'=\'".join(string.split("="))
    return string

RANDOM_KEY = random_bytes(16)
NONCE = random_bytes(8)

def oracle_encrypt_function(message):
    message = quote_illegal_chars(message)
    message_bytes = b"comment1=cooking%20MCs;userdata=" + str.encode(message) + b";comment2=%20like%20a%20pound%20of%20bacon"
    encrypted_message = CTR_mode(RANDOM_KEY, NONCE, 16, message_bytes)
    return encrypted_message

def oracle_decrypt_function(message):
    user_info = CTR_mode(RANDOM_KEY, NONCE, 16, message)
    return b";admin=true;" in user_info

ciphertext = oracle_encrypt_function("test:admin<true:")
bytes_to_change = ciphertext[16*2:16*3]
changed_bytes = binary_xOR(bytes_to_change, b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01')
edited_message = ciphertext[:16*2] + changed_bytes + ciphertext[16*3:]
print(oracle_decrypt_function(edited_message))
