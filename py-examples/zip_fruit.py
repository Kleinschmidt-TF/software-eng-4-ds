# Example: sequence functions
items = ["Banana", "Apple", "Orange"]
qty = [1, 2, 3]

# first create a new calculate on qty
# then pair up with the fruit items
l = list(zip(items, map(lambda x: x*10, qty)))
print("Mapped & zipped:", l)

# now filter out for pairs that have the qty > 10
l2 = list(filter(lambda x: x[1] > 10, l))
print("Filtered:",l2)

