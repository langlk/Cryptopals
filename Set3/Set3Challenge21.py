# Cryptopals
# Set 3 Challenge 21

# Implement Mersenne Twister

# I think? Used the python implementation from here:
# https://en.wikipedia.org/wiki/Mersenne_Twister

def _int32(x):
    return int(0xFFFFFFFF & x)

class MersenneTwister:
    def __init__(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i-1] ^ self.mt[i-1] >> 30) + i)

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18

        self.index = self.index + 1

        return _int32(y)

    def twist(self):
        for i in range(624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

twister = MersenneTwister(12)
for i in range(12):
    print(str(twister.extract_number()))
