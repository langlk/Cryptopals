# Cryptopals
# Set 2 Challenge 14

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
RANDOM_PADDING = random_bytes(randint(5,10))

def random_encode(message):
    message = pad_PKCS_7(RANDOM_PADDING + message, 16)
    return AES_ECB_encrypt(message, RANDOM_KEY)

def oracle_function(message):
    b64_code = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    bytes_code = base64.b64decode(b64_code)
    return random_encode(message + bytes_code)

def get_duplicate(message, blocksize):
    blocks = {}
    for i in range(0, len(message), blocksize):
        block = message[i:i + blocksize]
        if block in blocks:
            return block
        else:
            blocks[block] = 1
    return False

def find_duplicate_end(message, zero_block, blocksize):
    for i in range(len(message) - blocksize, 0, -blocksize):
        block = message[i: i + blocksize]
        if block == zero_block:
            return i + blocksize

def decrypt_ECB(secret_string, test_bytes, start_index, blocksize):
    secret_string_length = len(secret_string)
    result = b''
    for counter in range(0, int(secret_string_length/blocksize)):
        for j in range(1, blocksize + 1):
            test_message = test_bytes + b'0' * (blocksize - j) + result
            encoded_blocks = []
            for i in range(256):
                test_block = test_message + bytes([i])
                encoded_message = oracle_function(test_block)
                encoded_blocks.append(encoded_message[start_index:start_index + (blocksize * (counter + 1))])
            encoded_one_less = oracle_function(test_message[:len(test_bytes) + blocksize-j])[start_index:start_index + (blocksize * (counter + 1))]
            answer = bytes([encoded_blocks.index(encoded_one_less)])
            result += answer
            print(result)
            if result[-1] in range (1, blocksize + 1) and secret_string_length-len(result) <= blocksize :
                 return result

test_bytes = b'0' * 100
encrypted_message = oracle_function(test_bytes)
zero_block_encrypted = get_duplicate(encrypted_message, 16)
print(zero_block_encrypted)

# we want to find the first block after the random prefix that isn't a zero_block
end_duplicate = find_duplicate_end(encrypted_message, zero_block_encrypted, 16)
# Need to move the non-duplicate to the start of a block
for i in range(1, 16):
    test_bytes = test_bytes + (b'0' * i)
    encrypted_message = oracle_function(test_bytes)
    new_end_duplicate = find_duplicate_end(encrypted_message, zero_block_encrypted, 16)
    if new_end_duplicate > end_duplicate:
        end_duplicate = new_end_duplicate
        break

print(len(test_bytes))
secret_string = encrypted_message[end_duplicate:]
print(decrypt_ECB(secret_string, test_bytes, end_duplicate, 16))
# Sometimes this isn't working - returns a bunch of 0 bytes. Not sure why, should probably fix
