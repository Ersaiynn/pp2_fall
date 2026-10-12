filename = input("file: ")

with open(filename, "r") as f:
    count = 0
    for line in f:
        count += 1

print("lines:", count)
