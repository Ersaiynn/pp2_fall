import os

path = input("path: ") or "."

items = os.listdir(path)
dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
files = [i for i in items if os.path.isfile(os.path.join(path, i))]

print("directories:", dirs)
print("files:", files)
print("all:", items)
