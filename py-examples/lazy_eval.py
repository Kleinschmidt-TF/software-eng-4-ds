# Example 1: define lazy function and use map
print("Create lazy function and evaluate...")
my_add = lambda a, b: a + b
print(type(my_add))

# evaluate lazy function, and map element-wise
l = list(map(my_add, [1, 2, 3], [4, 5, 6]))
print(l)

# Example 2: define lazy filter function and apply
print("\nDefine a lazy filter function...")


def my_check(a):
    return a > 10 and a % 2


print(my_check)

# apply lazy filter
l = list(filter(my_check, [1, 5, 10, 11, 12, 25]))
print(l)

# reduce function example
import functools

result = functools.reduce(lambda a, b: a if a > b else b,
                          [3, 4, 6, 9, 34, 12])
print("\nUse Reduction...")
print(result)
