# Cryptopals
# Set 2 Challenge 13

from random import randint

def parse_key_val(key_val_string):
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
        return "email=" + email + "&uid=10&role=user"

print(profile_for("kels@mail.com"))
print(profile_for("kels&@mail.com"))
