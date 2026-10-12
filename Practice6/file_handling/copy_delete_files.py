import os
import shutil

shutil.copy("sample.txt", "sample_copy.txt")

os.makedirs("backup", exist_ok=True)
shutil.copy2("sample.txt", os.path.join("backup", "sample_backup.txt"))

print(os.listdir("."))
print(os.listdir("backup"))

for path in ["sample_copy.txt", os.path.join("backup", "sample_backup.txt")]:
    if os.path.exists(path):
        os.remove(path)
        print("deleted", path)
    else:
        print("not found", path)

try:
    os.rmdir("backup")
    print("backup folder removed")
except OSError as e:
    print("cannot remove folder:", e)
