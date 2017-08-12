# Cryptopals
# Set 1 Challenge 7

import base64
from Crypto.Cipher import AES

# Open file, change from b64 to bytes
b64_codes = open('Challenge7Code.txt', 'r')
bytes_code = b""
for line in b64_codes:
    bytes_code += base64.b64decode(line[0:-1])

# Decrypt with AES in ECB
aes_cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
result = aes_cipher.decrypt(bytes_code)
print(result)
