# Cryptopals
# Set 1 Challenge 3

def binary_xOR(byte_code1,byte_code2): # takes two bytes objects, returns XOR of them as bytes object
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

def frequency_score(code):
  """
  Scores letter frequency of an code represented as a bytes object. Starts with code_score = 1, then for each character in the code, multiplies the code_score by the frequency of that letter. If not a space or a letter, multiplies by .0001 to penalize weird characters.
  Higher Frequency Score is better.
  Only works for codes of the same length.
  """
  letter_frequencies = {
    b' ': .1828,
    b'e': .1026,
    b't': .0752,
    b'a': .0653,
    b'o': .0615,
    b'n': .0571,
    b's': .0567,
    b'r': .0499,
    b'h': .0498,
    b'd': .0328,
    b'l': .0331,
    b'u': .0227,
    b'c': .0223,
    b'm': .0203,
    b'f': .0198,
    b'w': .0170,
    b'g': .0162,
    b'p': .0150,
    b'y': .0142,
    b'b': .0126,
    b'v': 0.0080,
    b'k': 0.0056,
    b'x': 0.0014,
    b'j': 0.0010,
    b'q': 0.0008,
    b'z': 0.0005
  }
  code_score = 1
  code = code.lower() # Checks as lowercase
  for i in range(len(code)):
    char = bytes([code[i]])
    if char in letter_frequencies:
      code_score *= letter_frequencies[char]
    else: # Some random character/punctuation
      code_score *= 0.0001
  return code_score

hex_code = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
bytes_code = bytes.fromhex(hex_code)
scores = {} # Stores scores of each character xOR'd against

"""
XORs the code against byte object made of one character.
Then scores the character frequency, and stores.
"""
for a in range(255): # not sure if only checking through 255 will work for ch6
  decoder_bytes = bytes([a])*len(bytes_code)
  result_bytes = binary_xOR(bytes_code,decoder_bytes)
  score = frequency_score(result_bytes)
  scores[score] = [chr(a),result_bytes]
  # storing the scores as the keys of this dictionary right now, but this is probably a terrible idea if two codekeys ever produce the same score
print(scores[max(scores.keys())])
