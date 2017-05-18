# Cryptopals
# Set 1 Challenge 5

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
    
def bin_to_ascii(bin_code): # changes binary code string to ascii string
  i = 0
  ascii_string = ""
  while i+8 <= len(bin_code):
    ascii_string += chr(int(bin_code[i:i+8],2))
    i += 8
  return ascii_string
  
def ascii_to_bin(ascii_string): # changes ascii string to binary string
  bin_code = ""
  for char in ascii_string:
    temp_code = str(bin(ord(char)))
    temp_code = temp_code[2:len(temp_code)] # Removes the binary prefix
    while len(temp_code) < 8: # Standardizes length
      temp_code = "0" + temp_code
    bin_code += temp_code
  return bin_code

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
  
def repeating_key_xOR(string,key): 
  """
  Takes a binary string and a binary key. Makes the key repeat for the length of the string, then does a binary xOR and returns the result
  """
  key_string = ""
  while len(key_string) < len(string):
      key_string += key
  key_string = key_string[0:len(string)]
  return binary_xOR(string,key_string)
  
string1 = "Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal"
key1 = "ICE"
binary_string = ascii_to_bin(string1)
binary_key = ascii_to_bin(key1)
# Make Key and String binary before passing to repeating key_xOR
binary_code_string = repeating_key_xOR(binary_string,binary_key)
hex_code_string = binary_to_hex(binary_code_string)
print(hex_code_string)
# Stuff below checks if this did the thing right
print(hex_code_string == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
print(bin_to_ascii(repeating_key_xOR(hex_to_binary(hex_code_string),binary_key)))
