new_lines = ["Farida 20 Taraz", "Gulnur 23 Oral"]

with open("sample.txt", "a") as f:
    for line in new_lines:
        f.write(line + "\n")

with open("sample.txt", "r") as f:
    data = f.read()

for line in new_lines:
    if line in data:
        print(line, "- ok")
    else:
        print(line, "- missing")

print(data)
