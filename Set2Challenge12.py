# Cryptopals
# Set 2 Challenge 12
import sys
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

def random_encode(message):
    message = pad_PKCS_7(message,16)
    return AES_ECB_encrypt(message, RANDOM_KEY)

def guess_ECB(message, blocksize):
    blocks = {}
    for i in range(0, len(message), blocksize):
        block = message[i:i + blocksize]
        if block in blocks:
            return True
        else:
            blocks[block] = 1
    return False

def oracle_function(message):
    b64_code = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    bytes_code = base64.b64decode(b64_code)
    return random_encode(message + bytes_code)

def detectBlockSize():
    plaintext = b'0' * 100
    encoded_message = oracle_function(plaintext)
    for i in range(1, 50):
        chunk_1 = encoded_message[0:i]
        chunk_2 = encoded_message[i:i*2]
        if chunk_1 == chunk_2:
            return i
    return -1

blocksize = detectBlockSize()
is_ECB = guess_ECB(oracle_function(b'0'*100), blocksize)
secret_string = oracle_function(b"")
secret_string_length = len(secret_string)
print(secret_string_length)

result = b''
for counter in range(0, int(secret_string_length/blocksize)):
    end_index = counter * blocksize + blocksize
    for j in range(1, blocksize + 1):
        test_message = b'0' * (blocksize - j) + result
        encoded_blocks = []
        for i in range(256):
            test_block = test_message + bytes([i])
            encoded_message = oracle_function(test_block)
            encoded_blocks.append(encoded_message[:counter*blocksize + blocksize])
        encoded_one_less = oracle_function(test_message[:blocksize-j])[:blocksize*counter + blocksize]
        answer = bytes([encoded_blocks.index(encoded_one_less)])
        result += answer
        print(result)
        if result[-1] in range (1, blocksize + 1) and secret_string_length-len(result) <= blocksize :
             print(result)
             sys.exit()
print(result)
