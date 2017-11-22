# Cryptopals
# Set 3 Challenge 23

# Clone an MT19937 from output

import MersenneTwister
import random

# Right shift:
# top *shift* bits are the top *shift* of the number
# once you have those, you can determine everything that came after because you have the shifted part and you can just shift and xor to get the rest
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

# bottom *shift* bits are the original number
# after that, next *shift* bits are original number xored with shifted number & magic number
def untemper_left(number, shift, magic_num):
    mask = int('1' * shift, 2)
    result = number & mask
    count = 1
    while shift * count < 32:
        mask = mask << shift
        count += 1
        shifted = result << shift & magic_num
        subresult = number ^ shifted
        result = result | (subresult & mask)
    return result & int('1' * 32, 2)

def untemper(number):
    number = untemper_right(number, 18)
    number = untemper_left(number, 15, 4022730752)
    number = untemper_left(number, 7, 2636928640)
    number = untemper_right(number, 11)
    return number

m = MersenneTwister.MersenneTwister(random.randint(0, 1000))
state = []

for i in range(624):
    output = m.extract_number()
    state.append(untemper(output))

m_copy = MersenneTwister.MersenneTwister(0)
m_copy.set_state(state)

for i in range(10):
    print("Orginal:", m.extract_number())
    print("Copy:   ", m_copy.extract_number())
