# Cryptopals
# Set 3 Challenge 19

# Break Fixed-Nonce CTR using substitutions

import base64
from Crypto.Cipher import AES
from random import randint

def random_bytes(n):
    random_ints = []
    for i in range(n):
        random_ints.append(randint(0,255))
    return bytes(random_ints)

def binary_xOR(byte_code1,byte_code2):
    result = b''
    for i in range(len(byte_code1)):
        result += bytes([byte_code1[i] ^ byte_code2[i]])
    return result

# Encrypt with AES in ECB
def AES_ECB_encrypt(bytes_code, key):
    aes_cipher = AES.new(key, AES.MODE_ECB)
    return aes_cipher.encrypt(bytes_code)

def CTR_mode(key, nonce, blocksize, message):
    ciphertext = b''
    counter = 0
    while len(ciphertext) < len(message):
        key_stream = AES_ECB_encrypt(nonce + (counter).to_bytes(8, byteorder="little"), key)
        block = message[blocksize * counter:blocksize * counter + blocksize]
        ciphertext += binary_xOR(key_stream[:len(block)], block)
        counter += 1
    return ciphertext
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

# Changes bytes object to a binary string
def bytes_to_binary(bytes_code):
    result = ""
    for i in range(len(bytes_code)):
        new_bin = str(bin(bytes_code[i]))[2:]
        while len(new_bin) < 8:
            new_bin = "0" + new_bin
        result += new_bin
    return result

# finds edit distance between 2 equal-length bytes objects
def edit_distance(bytes1,bytes2):
    binary_str1 = bytes_to_binary(bytes1)
    binary_str2 = bytes_to_binary(bytes2)
    distance = 0
    for i in range(len(binary_str1)):
        if binary_str1[i] != binary_str2[i]:
            distance += 1
    return distance

# Gets average edit distance between all keysize chunks in bytes_code
# Returns average divided by keysize to normalize
# Throws away some bytes at the end of bytes code
def avg_edit_distance(bytes_code, keysize):
    chunks = []
    for i in range(0, len(bytes_code) - keysize, keysize):
        chunks.append(bytes_code[i:i+keysize])
    total_distance = 0
    for i in range(len(chunks)-1):
        total_distance += edit_distance(chunks[i], chunks[i + 1])
    return total_distance / len(chunks) / keysize

# Returns list of bytes objects where the first object is the first byte of
# every keysize block, the second object is the second byte, etc
def make_transposed_blocks(bytes_code, keysize):
    transposed_blocks = [b""] * keysize
    i = 0
    j = 0
    while i < len(bytes_code):
        transposed_blocks[j] += bytes([bytes_code[i]])
        i += 1
        if (j < keysize - 1):
            j += 1
        else:
            j = 0
    return transposed_blocks

def break_xOR(bytes_code):
    # Get Hamming Distances
    normalized_edit_distances = []
    for keysize in range(2, 41):
        normalized_edit_distances.append(avg_edit_distance(bytes_code, keysize))

    # Get keys with lowest Hamming Distances
    best_keysizes = []
    for i in range(3):
        min_distance = min(normalized_edit_distances)
        min_distance_key = normalized_edit_distances.index(min_distance) + 2
        best_keysizes.append(min_distance_key)
        normalized_edit_distances[min_distance_key - 2] = 100

    # Gets the best key of each keysize
    best_keys = {}
    for key in best_keysizes:
        best_of_size = b""
        total_score = 0
        # Makes blocks of first byte of each keysize chunk, second, so on
        blocks = make_transposed_blocks(bytes_code, key)
        for block in blocks:
            # For each block, run single-char XOR detection algorithm
            scores = {}
            for a in range(256):
                decoder_bytes = bytes([a])*len(block)
                result_bytes = binary_xOR(block,decoder_bytes)
                score = frequency_score(result_bytes[0:100])
                scores[score] = bytes([a])
            # Add single-char key with best score to the full key
            max_score = max(scores.keys())
            best_of_size += scores[max_score]
            total_score += max_score
        # Save normalized score and full key
        best_keys[total_score/key] = best_of_size

    # Print out best key and diciphered text
    best_score = max(best_keys.keys())
    key = best_keys[best_score]
    print(key)
    decoder_bytes = key * (len(bytes_code)//len(key)) + key
    decoder_bytes = decoder_bytes[:len(bytes_code)]
    return binary_xOR(bytes_code,decoder_bytes)

# Set-up
RANDOM_KEY = random_bytes(16)
NONCE = b'\x00' * 8
plaintexts = open("Challenge19Codes.txt", "r")
ciphertexts = []
for line in plaintexts:
    ciphertexts.append(CTR_mode(RANDOM_KEY, NONCE, 16, base64.b64decode(line.strip())))

# Solving
first_blocks = b''
second_blocks = b''
for text in ciphertexts:
    first_blocks += text[:16]
    second_blocks += text[16:32]
    if len(text) < 32:
        second_blocks += b'0' * (32 - len(text))

decoded_first_block = break_xOR(first_blocks)
decoded_second_block = break_xOR(second_blocks)

for i in range(int(len(decoded_first_block) / 16)):
    print(decoded_first_block[i*16:i*16 + 16] + decoded_second_block[i*16:i*16 + 16])
