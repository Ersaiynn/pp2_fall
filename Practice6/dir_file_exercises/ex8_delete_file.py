import os

path = input("path: ")

if not os.path.exists(path):
    print("path does not exist")
elif not os.path.isfile(path):
    print("not a file")
elif not os.access(path, os.W_OK):
    print("no access")
else:
    os.remove(path)
    print("deleted")
