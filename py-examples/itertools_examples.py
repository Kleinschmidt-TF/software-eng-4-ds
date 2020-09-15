import itertools

# Example 1: use chain to combine two iterables in this order
print("Example 1: Chaining...")
for x in itertools.chain('abc', range(3)):
    print(x)

# Example 2: use product to do equivalent of zip
print("Example 2: Product...")
print(list(itertools.product('abc', range(3))))

# Example 3: create at iterable that can loop again!
print("Example 3: Cycling...")
infinite = iter(itertools.cycle('abc'))
print(next(infinite))
print(next(infinite))
print(next(infinite))
print(next(infinite))
print(next(infinite))