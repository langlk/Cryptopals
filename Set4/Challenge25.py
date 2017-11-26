# Cryptopals
# Set 4 Challenge 25

# Break "Random Access Read/Write" AES CTR

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

def CTR_edit(ciphertext, key, nonce, blocksize, offset, newtext):
    new_ciphertext = b''
    counter = 0
    offset_counter = offset
    while len(new_ciphertext) < len(newtext):
        keystream = AES_ECB_encrypt(nonce + (offset_counter).to_bytes(8, byteorder="little"), key)
        block = newtext[blocksize * counter:blocksize * counter + blocksize]
        new_ciphertext += binary_xOR(keystream[:len(block)], block)
        counter += 1
        offset_counter += 1
    return ciphertext[:blocksize * offset] + new_ciphertext + ciphertext[(blocksize * offset) + len(new_ciphertext):]

RANDOM_KEY = random_bytes(16)
NONCE = random_bytes(8)
plaintexts = open("Set3/Challenge20Codes.txt", "r")
plaintext = b''
for line in plaintexts:
    plaintext += base64.b64decode(line)
ciphertext = CTR_mode(RANDOM_KEY, NONCE, 16, plaintext)

recovered_plaintext = b''
for i in range(int(len(ciphertext) / 16) + 1):
    recovered_block = b''
    for j in range(16):
        for k in range(256):
            test_edit = CTR_edit(ciphertext, RANDOM_KEY, NONCE, 16, i, recovered_block + bytes([k]))
            if test_edit == ciphertext:
                recovered_block += bytes([k])
                break
    recovered_plaintext += recovered_block

print(recovered_plaintext)
if (recovered_plaintext == plaintext):
    print("It worked!")
