from typing import List, Tuple, Set
import re
from Levenshtein import ratio


# преобразование строк к идентичному виду
def normalize(line):
    line = line.lower().replace('ё', 'е')
    line = re.sub(r'[^\w\s]', '', line)  # удаляем символы пунктуации
    return ' '.join(line.split())  # удаляем лишние пробелы


# мера сходства строк
def similarity(line1, line2):
    if not line1 or not line2:
        return 0.0
    return ratio(line1, line2)


class Solution:
    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        return [self.find_chorus(lines) for lines, title in tracks]

    def find_chorus(self, lines):
        lines = [normalize(line) for line in lines]
        n = len(lines)

        # таблица сходства всех строк песни
        sim = [[similarity(lines[i], lines[j]) for j in range(n)] for i in range(n)]

        best_score = 0.0  # максимальная оценка
        best_blocks = set()  # границы припевов для максимальной оценки

        # перебираем всевозможные длины припевов
        for size in range(2, n // 2 + 1):
            # всевозможные варианты начала первого припева заданной длины
            for i in range(n - size + 1):
                positions = [i]  # начало припева
                score = 0.0

                # ищем похожие фрагменты после образца
                for j in range(i + size, n - size + 1):
                    # пропускаем пересекающиеся фрагменты
                    if j < positions[-1] + size:
                        continue

                    # сходство строк в среднем
                    match = sum(sim[i + k][j + k] for k in range(size)) / size
                    
                    if match >= 0.8:  # порог подобран экспериментально
                        positions.append(j)
                        score += size * match ** 7  # "баллы" за каждое найденное повторение

                if score > best_score:
                    best_score = score
                    best_blocks = {(j, j + size - 1) for j in positions}

        return best_blocks