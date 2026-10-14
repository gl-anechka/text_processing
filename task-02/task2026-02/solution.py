from typing import List, Tuple, Set
import re
from functools import lru_cache

# преобразование строк к идентичному виду
def normalize(line):
    line = line.lower().replace('ё', 'е')
    line = re.sub(r'[^\w\s]', '', line)  # удаляем символы пунктуации
    return ' '.join(line.split())  # пересобрали строку, чтобы не было лишних пробелов

# разбиваем предложение на биграммы
@lru_cache(maxsize=10000)
def bigrams(line):
    return set(line[i:i + 2] for i in range(len(line) - 1))

# мера сходства строк
def similarity(line1, line2):
    if line1 == line2:
        if line1:
            return 1.0
        else:
            return 0.0

    line1_bigram = bigrams(line1)
    line2_bigram = bigrams(line2)
    if not line1_bigram or not line2_bigram:
        return 0.0

    return 2 * len(line1_bigram & line2_bigram) / (len(line1_bigram) + len(line2_bigram))


class Solution:
    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        result = []
        for lines, _ in tracks:
            result.append(self.find_chorus(lines))
        return result

    # сравнение двух фрагментов одинаковой длины
    def similar_fragments(self, sim, i, j, size):
        values = [sim[i + k][j + k] for k in range(size)]  # k - смещение от начала сегмента
        average = sum(values) / size  # среднее сходство всех строк двух фрагментов
        return average >= 0.7

    # объединение начальных позиций похожих фрагментов
    def find_groups(self, sim, size):
        start_count = len(sim) - size + 1
        groups = []

        # всевозможные начальные позиции первого фрагмента
        for i in range(start_count):
            positions = [i]  # образец и его повторы
            for j in range(i + size, start_count):
                # повтор не должен пересекаться с предыдущим найденным
                if j >= positions[-1] + size and self.similar_fragments(sim, i, j, size):
                    positions.append(j)
            groups.append(positions)

        return groups

    # оценка качества группы повторяющихся фрагментов
    def group_score(self, sim, selected, size):
        first = selected[0]  # образец
        
        # сходство каждого фрагмента с первым
        matches = [sum(sim[first + k][j + k] for k in range(size)) / size for j in selected[1:]]
        quality = sum(matches) / len(matches)

        # длина * число повторов, а неточные совпадения сильно штрафуем степенью
        return size * len(selected) * quality ** 3

    # поиск припевов песни
    def find_chorus(self, lines):
        lines = [normalize(line) for line in lines]
        n = len(lines)
        if n < 4:
            return set()

        sim = [[similarity(lines[i], lines[j]) for j in range(n)] for i in range(n)]

        best_score = 0.0  # максимальная оценка
        best_blocks = set()  # границы припевов для максимальной оценки

        # перебираем всевозможные длины припевов
        for size in range(2, n // 2 + 1):
            for selected in self.find_groups(sim, size):
                if len(selected) < 2:
                    continue

                score = self.group_score(sim, selected, size)
                if score > best_score:
                    best_score = score
                    best_blocks = {(i, i + size - 1) for i in selected}

        return best_blocks