# Cryptopals
# Set 2 Challenge 9

# Takes message (as bytes object) and blocksize and pads using PKCS #7
# Get p = blocksize - length of message mod blocksize
# Append p to message p times
# If p == 0, append blocksize blocksize times
def pad_PKCS_7(message, blocksize):
    padding_amount = blocksize - len(message) % blocksize
    if padding_amount == 0:
        padding_amount = blocksize
    padding = bytes([padding_amount]) * padding_amount
    return message + padding

# Takes padded message as bytes, returns unpadded message
def unpad_PKCS_7(message):
    padding_amount = message[-1]
    return message[:-padding_amount]

padded_message = pad_PKCS_7(b"YELLOW SUBMARINE", 20)
print(padded_message)
print(unpad_PKCS_7(padded_message))
