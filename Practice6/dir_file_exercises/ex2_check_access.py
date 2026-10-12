import os

path = input("path: ")

print("exists:", os.access(path, os.F_OK))
print("readable:", os.access(path, os.R_OK))
print("writable:", os.access(path, os.W_OK))
print("executable:", os.access(path, os.X_OK))
