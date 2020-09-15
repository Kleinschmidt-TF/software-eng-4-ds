from collections import Counter, OrderedDict, namedtuple, ChainMap, deque

# N.B. in all examples, it will be listed by occurrence!
print("Counter collection...")
print("Initialization...")
# Example 1: define Counter by counting items per unique element in the list
print(Counter(['a', 'b', 'c', 'a', 'b', 'b']))

# Example 2: define Counter by passing in a set of key-value pairs
print(Counter({'a': 2, 'b': 1, 'c': 7}))

# Example 3: define Counter using arguments
print(Counter(a=2, b=5, c=4))

# accessing counts
print("\nAccessing...")
c = Counter(['a', 'b', 'c', 'a', 'b', 'b'])
# return just the elements, ordered by item
print(list(c.elements()))
# return the pairs, ordered from highest-occurrence to lowest
print(c.most_common())

# operations on the Counter
print("\nOperations...")
c1 = Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = Counter('abcdef')

print(c1)
print(c2)

print(f"Combined counts: {c1 + c2}")
print(f"Subtraction: {c1 - c2}")
print(f"Intersection: {c1 & c2}")

# TODO: play with other collections
# Ordereddict - order in which keys are added to the dictionary
print("\nOrdereddict...")
print("Initialization...")
d = OrderedDict.fromkeys('abcdeftkabcde')
d['t'] = 10

print("Initialized:", d)

d.move_to_end('c')
print("Reordered:", d)

d.popitem()
print("Popped last:", d)

d.popitem(last=False)
print("Popped first:", d)

# Namedtuple
print("\nNamed tuple...")
Point = namedtuple('Point', ['x', 'y'])

p = Point(11, y=2)
print(p)
print(f"Add elements: {p[0] + p[1]}")

# Chainmap - groups multiple dicts (or other mappings)
print("\nChainMap...")
baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
cmap = list(ChainMap(adjustments, baseline))
print(cmap)

# Deque - double-ended queue
print("\nDeque...")
d = deque('ghi')
print("Initialized:", d)

d.append('k')
d.appendleft('t')       # can add to the front of the queue!
print("Appended:", d)

print("Reversed:", deque(reversed(d)))
