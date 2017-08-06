# Cryptopals
# Set 1 Challenge 5

def binary_xOR(byte_code1,byte_code2): # takes two bytes objects, returns XOR of them as bytes object
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

message = "Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

# Make Key and String bytes before passing to repeating key_xOR
bytes_message = bytes(message, "ascii")
bytes_key = bytes(key, "ascii")

# Make repeating key of same length as message.
repeating_bytes_key = bytes_key * int(len(bytes_message)/len(bytes_key)) + bytes(bytes_key[:len(bytes_message)%len(bytes_key)])

# XOR and change to hex
coded_bytes = binary_xOR(bytes_message, repeating_bytes_key)
hex_code = coded_bytes.hex()

print(hex_code)
if hex_code == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f":
    print("It worked!")
