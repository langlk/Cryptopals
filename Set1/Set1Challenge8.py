# Cryptopals
# Set 1 Challenge 8

from Crypto.Cipher import AES

hex_codes = open('Challenge8Codes.txt', 'r')
bytes_codes = []
for line in hex_codes:
    bytes_code = bytes.fromhex(line[0:-1])
    bytes_codes.append(bytes_code)

# Checks if code has any repeated 16-byte blocks. If so, sets answer to that code
answer = b""
for code in bytes_codes:
    blocks = {}
    for i in range(0, len(code), 16):
        block = code[i:i + 16]
        if block in blocks:
            answer = code
        else:
            blocks[block] = 1

print("The encoded block is line number " + str(bytes_codes.index(answer) + 1))
