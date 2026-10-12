values = [10, 3.14, "hello", True, [1, 2], (1, 2), {"a": 1}, {1, 2}, None]

for v in values:
    print(v, type(v))

print(isinstance(10, int))
print(isinstance(10, float))
print(isinstance("a", (int, str)))
print(isinstance(True, int))

print(int("42"))
print(int(3.9))
print(float("2.5"))
print(float(7))
print(str(123))
print(bool(0), bool(1), bool(""), bool("a"))
print(list("abc"))
print(tuple([1, 2, 3]))
print(set([1, 1, 2, 3]))

try:
    int("abc")
except ValueError as e:
    print("error:", e)
