# Cryptopals
# Set 1 Challenge 6

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

def b64_char_to_bin(char): #decodes base 64 character into binary
	if char == "=":
		return "000000"
	base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	bin_char = bin(base64Chars.find(char))
	bin_char = bin_char[2:len(bin_char)]
	while len(bin_char) < 6:
		bin_char = "0" + bin_char
	return bin_char 

def base64_to_binary(b64_code): #decodes base64 string to binary string 
  bin_string = ""
  for char in b64_code:
	  bin_string += b64_char_to_bin(char)
  return bin_string
  
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

def frequency_score(code):
  """
  Scores letter frequency of an ascii string. Starts with code_score = 1, then for each character in the code, multiplies the code_score by the frequency of that letter. If not a space or a letter, multiplies by .0001 to penalize weird characters. 
  Higher Frequency Score is better.
  Only works for strings of the same length.
  """
  letter_frequencies = {
    ' ': .1828,
    'e': .1026, 
    't': .0752,
    'a': .0653,
    'o': .0615,
    'n': .0571,
    's': .0567,
    'r': .0499,
    'h': .0498,
    'd': .0328,
    'l': .0331,
    'u': .0227,
    'c': .0223,
    'm': .0203,
    'f': .0198,
    'w': .0170,
    'g': .0162,
    'p': .0150,
    'y': .0142,
    'b': .0126,
    'v': 0.0080,
    'k': 0.0056,
    'x': 0.0014,
    'j': 0.0010,
    'q': 0.0008,
    'z': 0.0005
  }
  code_score = 1
  for char in code.lower(): # Checks as lowercase
    if char in letter_frequencies:
      code_score *= letter_frequencies[char]
    else: # Some random character/punctuation
      code_score *= 0.0001
  return code_score

def edit_distance(str1,str2): # finds edit distance between 2 equal-length binary strings
	x = 0
	distance = 0
	while x < len(str1):
		if str1[x] != str2[x]:
			distance += 1 
		x += 1 
	return distance

#SO NOT FINISHED YET
def make_blocks(code_string,keysize): # code_string is binary, keysize in bytes
  block_length = keysize*8 # keysize is in bytes, change to bits
  keysize_blocks = [code_string[i:i+block_length] for i in range(0, len(code_string), block_length)]
  transposed_blocks = []
  

codes = open('Challenge6Codes.txt', 'r')
code = ""
for line in codes:
  code += line[0:-1]
binary_code = base64_to_binary(code)

print(binary_code)
# Get Hamming Distances  
normalized_edit_distances = []  
for keysize in range(2,41):
  chunk_one = binary_code[0:keysize*8]
  chunk_two = binary_code[keysize*8:keysize*8*2]
  edit_dist = edit_distance(chunk_one,chunk_two)
  normalized_edit_distances.append(edit_dist/float(keysize))
# Get 3 keysizes with the smallest Hamming Distance
keysizes = []
for i in range(3):
  min_distance_key = normalized_edit_distances.index(min(normalized_edit_distances)) + 2 
  keysizes.append(min_distance_key)
  normalized_edit_distances[min_distance_key - 2] = 100

for keysize in keysizes:
  make_blocks(binary_code,keysize) 
