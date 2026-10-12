import re

text = "Hello World ABC Python rEgex Test"
print(re.findall(r"[A-Z][a-z]+", text))
