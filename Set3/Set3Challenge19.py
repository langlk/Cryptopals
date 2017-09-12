# Cryptopals
# Set 3 Challenge 19

# Break Fixed-Nonce CTR using substitutions

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

RANDOM_KEY = random_bytes(16)
NONCE = b'\x00' * 8
plaintexts = open("Challenge19Codes.txt", "r")
ciphertexts = []
for line in plaintexts:
    ciphertexts.append(CTR_mode(RANDOM_KEY, NONCE, 16, base64.b64decode(line.strip())))
print(ciphertexts)
