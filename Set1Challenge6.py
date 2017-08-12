# Cryptopals
# Set 1 Challenge 6
import base64

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

def bytes_to_binary(bytes_code): # Changes bytes object to a binary string
    result = ""
    for i in range(len(bytes_code)):
        new_bin = str(bin(bytes_code[i]))[2:]
        while len(new_bin) < 8:
            new_bin = "0" + new_bin
        result += new_bin
    return result

def edit_distance(bytes1,bytes2): # finds edit distance between 2 equal-length bytes objects
    binary_str1 = bytes_to_binary(bytes1)
    binary_str2 = bytes_to_binary(bytes2)
    distance = 0
    for i in range(len(binary_str1)):
        if binary_str1[i] != binary_str2[i]:
            distance += 1
    return distance

# Open file, change lines from b64 to bytes
b64_codes = open('Challenge6Code.txt', 'r')
bytes_code = b""
for line in b64_codes:
    bytes_code += base64.b64decode(line[0:-1])

# Get Hamming Distances
normalized_edit_distances = []
for keysize in range(2, 41):
    chunk_one = bytes_code[0:keysize]
    chunk_two = bytes_code[keysize:keysize*2]
    edit_dist = edit_distance(chunk_one, chunk_two)
    normalized_edit_distances.append(edit_dist/float(keysize))

# Get keys with lowest Hamming Distances
best_keys = []
for i in range(3):
    min_distance = min(normalized_edit_distances)
    min_distance_key = normalized_edit_distances.index(min_distance) + 2
    best_keys.append(min_distance_key)
    normalized_edit_distances[min_distance_key - 2] = 100

#SO NOT FINISHED YET
# def make_blocks(code_string,keysize): # code_string is binary, keysize in bytes
#   block_length = keysize*8 # keysize is in bytes, change to bits
#   keysize_blocks = [code_string[i:i+block_length] for i in range(0, len(code_string), block_length)]
#   transposed_blocks = []

# for keysize in keysizes:
#   make_blocks(binary_code,keysize)
