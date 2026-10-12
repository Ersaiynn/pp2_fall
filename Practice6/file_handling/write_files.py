lines = [
    "Alice 20 Almaty",
    "Bob 21 Astana",
    "Dana 19 Shymkent",
    "Erlan 22 Aktau",
]

with open("sample.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

print("file created")
