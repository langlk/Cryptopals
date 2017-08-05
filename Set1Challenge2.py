# Cryptopals
# Set 1 Challenge 2

def binary_xOR(byte_code1,byte_code2): # takes two bytes objects, returns XOR of them as bytes object
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

hex_code1 = "1c0111001f010100061a024b53535009181c"
hex_code2 = "686974207468652062756c6c277320657965"

# Change hex codes into bytes object
bytes_code1 = bytes.fromhex(hex_code1)
bytes_code2 = bytes.fromhex(hex_code2)

# XOR the two codes and change back to hex
bytes_result = binary_xOR(bytes_code1,bytes_code2)
hex_result = bytes_result.hex()

if("746865206b696420646f6e277420706c6179" == hex_result):
    print("It Works!")

print(hex_result)
