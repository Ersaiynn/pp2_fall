names = ["Alice", "Bob", "Dana"]
ages = [20, 21, 19]
cities = ["Almaty", "Astana", "Shymkent"]

for i, name in enumerate(names):
    print(i, name)

for i, name in enumerate(names, start=1):
    print(i, name)

for name, age in zip(names, ages):
    print(name, age)

for name, age, city in zip(names, ages, cities):
    print(name, age, city)

for i, (name, age) in enumerate(zip(names, ages)):
    print(i, name, age)

people = dict(zip(names, ages))
print(people)

pairs = list(zip(names, ages))
n, a = zip(*pairs)
print(n)
print(a)
