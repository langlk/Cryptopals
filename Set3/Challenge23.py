# Cryptopals
# Set 3 Challenge 23

# Clone an MT19937 from output

import MersenneTwister

# Right shift:
# top 18 bits are the top 18 of the number
# once you have those, you can determin everything that came after because you have the shifted part and you can just shift and xor to get the rest
def untemper_right(number, shift):
    mask = int(('1' * shift), 2) << (32 - shift)
    result = number & mask
    shifted = result >> shift
    mask = mask >> shift
    result_part_two = (result >> shift) ^ (number & mask)
    result = result | result_part_two
    if shift * 2 <= 32:
        mask = int('1' * (32 - (shift * 2)), 2)
        result_part_three = ((result >> shift) & mask)^ (number & mask)
        result = result | result_part_three
    return result

m = MersenneTwister.MersenneTwister(1)

test = m.extract_number()
