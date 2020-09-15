# Example: unpacking (advanced - create a list)
first, *all, last = range(100)

print(f"First: {first}")
print(f"Sum of middle: {sum(all)}")
print(f"Last: {last}")
print("All middle: ", all)
