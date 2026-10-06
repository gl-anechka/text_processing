from typing import List, Tuple, Set


class Solution:
    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        return [set() for lines, title in tracks]
