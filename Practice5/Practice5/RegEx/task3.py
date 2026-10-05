import re

text = "hello_world test_case Not_match another_one a_b abc"
print(re.findall(r"\b[a-z]+_[a-z]+\b", text))
