import re

pattern = r"^a.*b$"

for s in ["ab", "axxxb", "a123b", "abc", "ba", "acb"]:
    print(s, bool(re.fullmatch(pattern, s)))
