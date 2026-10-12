import os
import glob

ext = ".py"

for root, dirs, files in os.walk("."):
    for name in files:
        if name.endswith(ext):
            print(os.path.join(root, name))

print(glob.glob("**/*.txt", recursive=True))
print(glob.glob("*" + ext))
