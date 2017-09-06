# Cryptopals
# Set 2 Challenge 13

from Crypto.Cipher import AES
from random import randint

# Decrypt with AES in ECB
def AES_ECB_decrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.decrypt(bytes_code)

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

def pad_PKCS_7(message, blocksize):
    padding_amount = blocksize - len(message) % blocksize
    if padding_amount == 0:
        padding_amount = blocksize
    padding = bytes([padding_amount]) * padding_amount
    return message + padding

def unpad_PKCS_7(message, blocksize):
    padding_amount = message[-1]
    return message[:-padding_amount]

def random_bytes(n):
    random_ints = []
    for i in range(n):
        random_ints.append(randint(0,255))
    return bytes(random_ints)

RANDOM_KEY = random_bytes(16)

def random_encode(message):
    message = pad_PKCS_7(message,16)
    return AES_ECB_encrypt(message, RANDOM_KEY)

def parse_key_val(encoded_string):
    key_val_string = str(unpad_PKCS_7(AES_ECB_decrypt(encoded_string, RANDOM_KEY), 16))[2:-1]
    key_val_list = key_val_string.split("&")
    key_val_obj = {}
    for pair in key_val_list:
        key_val = pair.split("=")
        key_val_obj[key_val[0]] = key_val[1]
    return key_val_obj

def profile_for(email):
    if (email.find("&") != -1 or email.find("=") != -1):
        return "Invalid Email"
    else:
        profile_string = "email=" + email + "&uid=10&role=user"
        encoded_profile = random_encode(bytes(profile_string, 'ascii'))
        return encoded_profile

test = profile_for("kels@mail.com")
print(test)
print(parse_key_val(test))

# need to figure out ciphertext that produces "&role=admin" without being able to feed & or = into profile_for
test_email_1 = "kels@mail.com"
test_encode = profile_for(test_email_1)
email_code = test_encode[:16]
uid_role_garbage = test_encode[16:32]
test_email_2 = ("0" * 10) + "admin" + ("\x0b" * 11)
test_encode = profile_for(test_email_2)
admin_chunk = test_encode[16:32]
print(parse_key_val(email_code + uid_role_garbage + admin_chunk))
