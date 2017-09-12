# Set 3
# Challenge 18

# Implement CTR

import base64
from Crypto.Cipher import AES

def binary_xOR(byte_code1,byte_code2):
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

# Encrypt/Decrypt CTR mode
def CTR_mode(key, nonce, blocksize, message):
    ciphertext = b''
    counter = 0
    while len(ciphertext) < len(message):
        key_stream = AES_ECB_encrypt(nonce + (counter).to_bytes(8, byteorder="little"), key)
        block = message[blocksize * counter:blocksize * counter + blocksize]
        ciphertext += binary_xOR(key_stream[:len(block)], block)
        counter += 1
    return ciphertext

key = b'YELLOW SUBMARINE'
nonce = b'\x00' * 8
message = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

print(CTR_mode(key, nonce, 16, message))
