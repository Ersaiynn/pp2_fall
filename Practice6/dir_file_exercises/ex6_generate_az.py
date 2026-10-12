import os
import string

os.makedirs("letters", exist_ok=True)

for letter in string.ascii_uppercase:
    with open(os.path.join("letters", letter + ".txt"), "w") as f:
        f.write(letter)

print(len(os.listdir("letters")), "files created")
