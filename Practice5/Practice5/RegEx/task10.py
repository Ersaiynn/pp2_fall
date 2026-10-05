import re

s = "camelCaseStringExample"
print(re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower())
