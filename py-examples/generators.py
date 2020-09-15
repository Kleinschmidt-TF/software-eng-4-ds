# Example 1: generator definition
# define the generator
def get_even(number):
    for nb in range(number):
        if nb % 2 == 0:
            yield nb


# create the generator object get_even
c = get_even(20)
print(c)

print(type(c))

print(list(c))
print(c)

# Example 2: putting a generator expression inside ()
gen = (nb for nb in range(20) if nb % 2 == 0)
print("Generator expression:", list(gen))


# # Example 3: generator chaining
# # Use generator chaining to load one column at a time
# from itertools import islice
# import pandas as pd
# import numpy as np
#
# # Example only - file doesn't exist!
# a = islice(open("./tmp/stores.csv"), 1, None)
# b = map(lambda _: _.split(','), a)
# c = map(lambda _: np.median(_[1:25]), b)
#
# df = pd.DataFrame(list(c))


# Example 4: prime number generator
from typing import Generator


def take(n, gen):
    """Take the first n numbers from the generator"""
    res = []
    for _ in range(n):
        res.append(next(gen))

    return res


def prime_gen() -> Generator[int, None, None]:
    """Prime number generator"""
    yield 2
    yield 3
    prime_set = {2, 3}
    current_number = 5
    while True:
        if all(map(lambda _: current_number % _ != 0, prime_set)):
            yield current_number
            prime_set |= {current_number}
        current_number += 2


print("Example 4: ", take(15, prime_gen()))
