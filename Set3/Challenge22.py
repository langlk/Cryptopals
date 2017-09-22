# Cryptopals
# Set 3 Challenge 22

# Crack an MT19937 seed

import MersenneTwister
import time
import random

time.sleep(random.randint(40, 1000))
seed = int(time.time())
twister = MersenneTwister(seed)
time.sleep(random.randint(40, 1000))
print(twister.extract_number())
