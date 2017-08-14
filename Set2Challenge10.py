# Cryptopals
# Set 2 Challenge 10

import base64
from Crypto.Cipher import AES

# Decrypt with AES in ECB
def AES_ECB_decrypt(bytes_code):
    aes_cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    return aes_cipher.decrypt(bytes_code)

def AES_ECB_encrypt(bytes_code):
    aes_cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

b64_codes = open('Challenge7Code.txt', 'r')
bytes_code = b""
for line in b64_codes:
    bytes_code += base64.b64decode(line[0:-1])

decoded_bytes = AES_ECB_decrypt(bytes_code)
print(decoded_bytes)

encoded_bytes = AES_ECB_encrypt(decoded_bytes)
print(encoded_bytes == bytes_code)
