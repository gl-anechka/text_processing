import re
from solution import EXPRESSION_REGEXP

regexp = re.compile(EXPRESSION_REGEXP)
text = "(     63393394.98 /8505     )"

entities = set() 
for match in regexp.finditer(text): 
    for key, value in match.groupdict().items(): 
        if value is not None: 
            start, end = match.span(key) 
            entities.add((start, end, key))

entities = list(entities)
entities.sort()
for i in range(len(entities)):
    print(entities[i])