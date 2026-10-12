import os
import shutil

os.makedirs("source", exist_ok=True)
os.makedirs("dest", exist_ok=True)

for name in ["a.txt", "b.txt", "c.txt"]:
    with open(os.path.join("source", name), "w") as f:
        f.write("file " + name)

shutil.copy("source/a.txt", "dest/a_copy.txt")
shutil.move("source/b.txt", "dest/b.txt")

print("source:", os.listdir("source"))
print("dest:", os.listdir("dest"))
