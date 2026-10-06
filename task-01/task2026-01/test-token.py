import re
from solution import SERIES_REGEXP
import time

with open('../examples-task2026-01/series/95232.html', encoding='utf-8') as f:
    html = f.read()

start = time.time()
regexp = re.compile(SERIES_REGEXP)

entities = set()

for match in regexp.finditer(html):
    for key, value in match.groupdict().items():
        if value is not None:
            start, end = match.span(key)
            entities.add((start, end, key, value))

for entity in entities:
    print(entity)

print(time.time() - start)