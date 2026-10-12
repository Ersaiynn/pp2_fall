import os

os.makedirs("project/src/utils", exist_ok=True)
os.makedirs("project/docs/images", exist_ok=True)
os.makedirs("project/tests", exist_ok=True)

for name in ["project/main.py", "project/src/app.py", "project/docs/readme.txt", "project/tests/test_app.py"]:
    with open(name, "w") as f:
        f.write("")

for item in os.listdir("project"):
    path = os.path.join("project", item)
    if os.path.isdir(path):
        print("folder:", item)
    else:
        print("file:", item)

for root, dirs, files in os.walk("project"):
    print(root, dirs, files)
