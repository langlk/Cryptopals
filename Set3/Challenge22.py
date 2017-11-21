# Cryptopals
# Set 3 Challenge 22

# Crack an MT19937 seed

import MersenneTwister
import time
import random

# Impatient version

start_time = int(time.time())
seed = start_time + random.randint(40, 1000)
twister = MersenneTwister.MersenneTwister(seed)
result = twister.extract_number()
print(result)

for i in range(2050):
    twist = MersenneTwister.MersenneTwister(start_time + i)
    if twist.extract_number() == result:
        print("Seed is " + str(start_time + i))

# Patience-required version

time.sleep(random.randint(40, 1000))
seed = int(time.time())
twister = MersenneTwister.MersenneTwister(seed)
time.sleep(random.randint(40, 1000))
result = twister.extract_number()
print(result)

end_time = int(time.time())
for i in range(2050):
    twist = MersenneTwister.MersenneTwister(end_time - i)
    if twist.extract_number() == result:
        print("Seed is " + str(end_time - i))
