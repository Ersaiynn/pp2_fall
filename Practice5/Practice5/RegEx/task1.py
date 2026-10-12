import re

pattern = r"^ab*$"

for s in ["a", "ab", "abbb", "b", "abc", "ba"]:
    print(s, bool(re.fullmatch(pattern, s)))
