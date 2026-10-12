import re

s = "snake_case_string_example"
print(re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s))
