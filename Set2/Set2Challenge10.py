# Cryptopals
# Set 2 Challenge 10

import base64
from Crypto.Cipher import AES

# takes two bytes objects, returns XOR of them as bytes object
def binary_xOR(byte_code1,byte_code2):
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

# Decrypt with AES in ECB
def AES_ECB_decrypt(bytes_code):
    aes_cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    return aes_cipher.decrypt(bytes_code)

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code):
    aes_cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

# Encrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_encrypt(bytes_code, blocksize):
    encrypted_block = bytes([0]) * blocksize
    final_code = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        xORblock = binary_xOR(block, encrypted_block)
        encrypted_block = AES_ECB_encrypt(xORblock)
        final_code += encrypted_block
    return final_code

# Decrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_decrypt(bytes_code, blocksize):
    encrypted_block = bytes([0]) * blocksize
    final_message = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        decrypted_block = AES_ECB_decrypt(block)
        xORblock = binary_xOR(decrypted_block, encrypted_block)
        final_message += xORblock
        encrypted_block = block
    return final_message

b64_codes = open('Challenge10Code.txt', 'r')
bytes_code = b""
for line in b64_codes:
    bytes_code += base64.b64decode(line[0:-1])

decrypted_message = CBC_decrypt(bytes_code, 16)
print(decrypted_message)
encrypted_message = CBC_encrypt(decrypted_message, 16)
print("New Encrypted is same as original: " + str(encrypted_message == bytes_code))
