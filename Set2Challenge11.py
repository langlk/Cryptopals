# Cryptopals
# Set 2 Challenge 11

from Crypto.Cipher import AES
from random import randint

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

# Encrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_encrypt(bytes_code, key, blocksize):
    encrypted_block = bytes([0]) * blocksize
    final_code = b''
    for i in range(0, len(bytes_code), blocksize):
        block = bytes_code[i:i + blocksize]
        xORblock = binary_xOR(block, encrypted_block)
        encrypted_block = AES_ECB_encrypt(xORblock, key)
        final_code += encrypted_block
    return final_code

# Decrypt with CBC, IV = b'\x00'*blocksize, key="YELLOW SUBMARINE"
def CBC_decrypt(bytes_code, key, blocksize):
    encrypted_block = bytes([0]) * blocksize
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

def random_bytes(n):
    random_ints = []
    for i in range(n):
        random_ints.append(randint(0,255))
    return bytes(random_ints)

def random_padding(message):
    front_padding = random_bytes(randint(5,10))
    end_padding = random_bytes(randint(5,10))
    return front_padding + message + end_padding

def random_encode(message):
    message = pad_PKCS_7(random_padding(message),16)
    key = random_bytes(16)
    to_ECB = randint(0,1) == 0
    if to_ECB:
        return [AES_ECB_encrypt(message, key), to_ECB]
    else:
        return [CBC_encrypt(message, key, 16), to_ECB]

def guess_ECB(message, blocksize):
    blocks = {}
    for i in range(0, len(encoded_message), blocksize):
        block = encoded_message[i:i + blocksize]
        if block in blocks:
            return True
        else:
            blocks[block] = 1
    return False

message_input = ""
while(message_input != b"q"):
    message_input = bytes(input("Enter a message: "), "ascii")
    encoding_results = random_encode(message_input)
    encoded_message = encoding_results[0]
    is_ECB = encoding_results[1]

    guess = guess_ECB(encoded_message, 16)
    print(encoded_message)
    print("GuessECB: "+str(guess))
    print("IsECB: "+str(is_ECB))
    if (guess == is_ECB):
        print("You did it!")
