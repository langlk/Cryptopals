# Cryptopals
# Set 1 Challenge 1
import base64

code =  "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

byte_code = bytes.fromhex(code) # Get bytes object from hex string
b64_code = base64.b64encode(byte_code) # Encode bytes object as base64
b64_string = str(b64_code)[2:-1] # Change to string and remove bytes object crap

if ("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t" == b64_string): # Check that output is correct
    print("It works!")
    print(b64_string)
