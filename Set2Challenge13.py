# Cryptopals
# Set 2 Challenge 13

def parse_key_val(key_val_string):
    key_val_list = key_val_string.split("&")
    key_val_obj = {}
    for pair in key_val_list:
        key_val = pair.split("=")
        key_val_obj[key_val[0]] = key_val[1]
    return key_val_obj
