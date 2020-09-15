l = ("madam", "freer", "kayak", "kiosk")

# find the palindrome using list indexing
# to reverse you go [start:end:step], but start = 0 and end = len(l) are the defaults
pal = list(filter
           (lambda word: word == word[::-1],
            l))

print(pal)

# testing the syntax
# N.B. effectively the slice is [start:end:step]
print(l[1][0::2])
