import re

s = "SplitAtUpperCaseLetters"
print(re.findall(r"[A-Z][^A-Z]*", s))
