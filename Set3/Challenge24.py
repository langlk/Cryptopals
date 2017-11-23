# Cryptopals
# Set 3 Challenge 24

# Create MT19937 Stream Cipher and break

import MersenneTwister

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

test = MT_stream_cipher(b'testing', 1)
print(test)
print(MT_stream_cipher(test, 1))
