import json
from pathlib import Path
from solution import Solution

# проверка работы алгоритма по метрикам

def main():
    path = Path(__file__).parent.parent / 'examples-task2026-02' / 'tracks.json'
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

    tracks = [(track['lines'], track['title']) for track in data]
    expected = [{tuple(pair) for pair in track['chorus']} for track in data]
    predicted = Solution().detect(tracks)

    assert len(predicted) == len(expected)

    correct = sum(len(pred & exp) for pred, exp in zip(predicted, expected))

    predicted_count = sum(len(pred) for pred in predicted)
    expected_count = sum(len(exp) for exp in expected)

    precision = correct / predicted_count if predicted_count else 0
    recall = correct / expected_count if expected_count else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

    print(f'Песен: {len(tracks)}')
    print(f'Правильных припевов: {expected_count}')
    print(f'Найденных припевов: {predicted_count}')
    print(f'Точных совпадений: {correct}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1: {f1:.4f}')

if __name__ == '__main__':
    main()