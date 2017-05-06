# Cryptopals
# Set 1 Challenge 1

def hex_to_binary(hex_code): # Takes hex code as string, returns binary as string
  bin_code = ""
  i = 0
  while i+2 <= len(hex_code):
    temp_code = str(bin(int(hex_code[i:i+2], 16)))
    temp_code = temp_code[2:len(temp_code)] # Removes the binary prefix
    while len(temp_code) < 8: # Standardizes length
      temp_code = "0" + temp_code
    bin_code += temp_code
    i += 2
  return bin_code

def binary_to_base64(bin_code): # Takes binary as string, returns base64 code as string
  i = 0
  base64_translator = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
  base64_code = ""
  while i+6 <= len(bin_code):
      b = int(bin_code[i:i+6], 2)
      base64_code += base64_translator[b:b+1]
      i += 6
  return base64_code
  
code = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
result = binary_to_base64(hex_to_binary(code))
print("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t" == result) # Check that output is correct
print(binary_to_base64(hex_to_binary(code)))
