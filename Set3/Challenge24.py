# Cryptopals
# Set 3 Challenge 24

# Create MT19937 Stream Cipher and break

import MersenneTwister
import random

def binary_xOR(byte_code1,byte_code2):
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

def MT_stream_cipher(bytes_text, seed):
    m = MersenneTwister.MersenneTwister(seed)
    output = b''
    while len(bytes_text) > 0:
        keynum = m.extract_number()
        textblock = bytes_text[:4]
        bytes_text = bytes_text[4:]
        keystream = keynum.to_bytes(4, byteorder='big')[:len(textblock)]
        output += binary_xOR(textblock, keystream)
    return output

def encode(message):
    seed = random.randint(0, 65536)
    for i in range(random.randint(5, 50)):
        message = chr(random.randint(0, 256)) + message
    byte_message = message.encode('utf-8')
    return MT_stream_cipher(byte_message, seed)

secret_message = encode('A' * 14)

for i in range(65536):
    output = str(MT_stream_cipher(secret_message, i))
    if 'A' * 14 in output:
        print("Seed is:", i)
        print("Decoded:", output)
