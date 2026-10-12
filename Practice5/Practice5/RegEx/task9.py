import re

s = "InsertSpacesBetweenWordsStartingWithCapitals"
print(re.sub(r"(?<!^)(?=[A-Z])", " ", s))
