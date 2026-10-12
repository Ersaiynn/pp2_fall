from functools import reduce

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words = ["python", "file", "map", "reduce", "list"]

squares = list(map(lambda x: x * x, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))
lengths = list(map(len, words))
long_words = list(filter(lambda w: len(w) > 3, words))

total = reduce(lambda a, b: a + b, nums)
product = reduce(lambda a, b: a * b, nums[:5])
biggest = reduce(lambda a, b: a if a > b else b, nums)

print(squares)
print(evens)
print(lengths)
print(long_words)
print(total)
print(product)
print(biggest)
