fruits = ["apple", "banana", "orange", "mango", "kiwi"]

with open("list.txt", "w") as f:
    for item in fruits:
        f.write(item + "\n")

with open("list.txt", "r") as f:
    print(f.read())
