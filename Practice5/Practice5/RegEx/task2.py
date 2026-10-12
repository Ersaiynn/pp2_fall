import re

pattern = r"^ab{2,3}$"

for s in ["a", "ab", "abb", "abbb", "abbbb"]:
    print(s, bool(re.fullmatch(pattern, s)))
