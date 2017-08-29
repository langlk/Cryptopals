# Cryptopals
# Set 2 Challenge 15

def is_PKCS_7(plainbytes):
    for byte in plainbytes[len(plainbytes) - plainbytes[-1]:]:
        if byte != plainbytes[-1]:
            return False
    return True

def unpad_PKCS_7(message):
    if is_PKCS_7(message):
        padding_amount = message[-1]
        return message[:-padding_amount]
    else:
        raise ValueError("Not PKCS#7 Padded")

tests = [b"ICE ICE BABY\x04\x04\x04\x04",b"ICE ICE BABY\x05\x05\x05\x05", b"ICE ICE BABY\x01\x02\x03\x04"]

for test in tests:
    try:
        print(unpad_PKCS_7(test))
    except ValueError as err:
        print(err.args)
