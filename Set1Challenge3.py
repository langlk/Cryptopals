# Cryptopals
# Set 1 Challenge 3

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
  
def binary_to_hex(bin_code): # Takes binary as string, returns hex code as string
    i = 0
    hex_code = ""
    while i+8 <= len(bin_code):
        temp_code = str(hex(int(bin_code[i:i+8],2)))
        temp_code = temp_code[2:len(temp_code)] # Remove prefix
        while len(temp_code) < 2: # standardizes length
            temp_code = "0" + temp_code
        hex_code += temp_code
        i += 8
    return hex_code
    
def binary_xOR(str1,str2): # takes two binary code strings, returns XOR of them as string
    a = 0
    newcode = ""
    while a+1 <= len(str1):
        b1 = str1[a]
        b2 = str2[a]
        if b1 != b2:
            newcode += "1"
        else:
            newcode += "0"
        a += 1
    return newcode
    
def bin_to_ascii(bin_code):
  i = 0
  ascii_string = ""
  while i+8 <= len(bin_code):
    ascii_string += chr(int(bin_code[i:i+8],2))
    i += 8
  return ascii_string
