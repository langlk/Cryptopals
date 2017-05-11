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
  
def ascii_to_bin(ascii_string):
  

def frequency_score(code):
  letter_frequencies = {
    ' ': 18.28,
    'e': 10.26, 
    't': 7.52,
    'a': 6.53,
    'o': 6.15,
    'n': 5.71,
    's': 5.67,
    'r': 4.99,
    'h': 4.98,
    'd': 3.28,
    'l': 3.31,
    'u': 2.27,
    'c': 2.23,
    'm': 2.03,
    'f': 1.98,
    'w': 1.70,
    'g': 1.62,
    'p': 1.50,
    'y': 1.42,
    'b': 1.26,
    'v': 0.80,
    'k': 0.56,
    'x': 0.14,
    'j': 0.10,
    'q': 0.08,
    'z': 0.05
  }
  code_frequencies = {}
  for char in code.lower():
    if char in code_frequencies:
      code_frequencies[char] += 1
    else:
      code_frequencies[char] = 1
  score = 0
  for char in code_frequencies.keys():
    if char in letter_frequencies:
      score += abs(letter_frequencies[char] - 100*(code_frequencies[letter]/len(code)))
    else:
      score += 100*(code_frequencies[letter]/len(code))
  return score

code = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
bin_code_1 = hex_to_binary(code)
for a in range(255):
  test_string = chr(a)*len(code)
