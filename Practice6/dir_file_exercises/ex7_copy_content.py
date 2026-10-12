src = input("source file: ")
dst = input("destination file: ")

with open(src, "r") as f1:
    data = f1.read()

with open(dst, "w") as f2:
    f2.write(data)

print("copied")
