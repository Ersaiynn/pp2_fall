import re

text = "Hello, world. Python is fun, right."
print(re.sub(r"[ ,.]", ":", text))
