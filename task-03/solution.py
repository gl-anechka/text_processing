from typing import List, Iterable, Set, Tuple


class Solution:
    def __init__(self):
        pass

    def predict(self, texts: List[str]) -> Iterable[Set[Tuple[int, int, str]]]:
        return [set() for _ in texts]
