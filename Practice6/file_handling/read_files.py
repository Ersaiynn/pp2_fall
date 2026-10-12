with open("sample.txt", "r") as f:
    content = f.read()
print(content)

with open("sample.txt", "r") as f:
    lines = f.readlines()
print(len(lines), "lines")

with open("sample.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(i, line.strip())
