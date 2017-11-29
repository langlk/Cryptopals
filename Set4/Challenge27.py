# Cryptopals
# Set 4 Challenge 27

# Recover Key from CBC where IV = Key

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
    initialization_vector = key
    encrypted_block = initialization_vector
    final_code = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        xORblock = binary_xOR(block, encrypted_block)
        encrypted_block = AES_ECB_encrypt(xORblock, key)
        final_code += encrypted_block
    return final_code

# Decrypt with CBC, IV = b'\x00'*blocksize
def CBC_decrypt(bytes_code, key, blocksize):
    initialization_vector = key
    encrypted_block = initialization_vector
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

def is_PKCS_7(plainbytes):
    for byte in plainbytes[len(plainbytes) - plainbytes[-1]:]:
        if byte != plainbytes[-1]:
            return False
    return True

def unpad_PKCS_7(message):
    if is_PKCS_7(message):
        padding_amount = message[-1]
        return message[:-padding_amount]
    else:
        raise ValueError("Not PKCS#7 Padded")

RANDOM_KEY = random_bytes(16)
RANDOM_PADDING = random_bytes(randint(5,10))

def quote_illegal_chars(string):
    string = "\';\'".join(string.split(";"))
    string = "\'=\'".join(string.split("="))
    return string

def test_ascii_compliance(message):
    for char_num in message:
        if char_num > 127:
            raise ValueError("Message contained invalid ascii characters: " + str(message)[2:-1])

def oracle_encrypt_function(message):
    message = quote_illegal_chars(message)
    message_bytes = b"comment1=cooking%20MCs;userdata=" + str.encode(message) + b";comment2=%20like%20a%20pound%20of%20bacon"
    encrypted_message = CBC_encrypt(pad_PKCS_7(message_bytes,16), RANDOM_KEY, 16)
    return encrypted_message

def oracle_decrypt_function(message):
    decrypted_message = CBC_decrypt(message, RANDOM_KEY, 16)
    user_info = unpad_PKCS_7(decrypted_message)
    return b";admin=true;" in user_info

test = CBC_encrypt(b'\x00' * 16, RANDOM_KEY, 16)
print(test)
print(test_ascii_compliance(CBC_decrypt(test, RANDOM_KEY, 16)))
