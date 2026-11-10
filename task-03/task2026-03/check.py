from solution import Solution
from pathlib import Path

# проверка итоговой модели на тесте для получения метрики

texts = []
answers = []

dev_dir = Path(__file__).parent.parent / 'NEREL-v1.1' / 'test'

for file in sorted(dev_dir.glob('*.txt')):
    texts.append(file.read_text(encoding='utf-8'))

    entities = set()
    for line in file.with_suffix('.ann').read_text(encoding='utf-8').splitlines():
        if line.startswith('T'):
            entity_type, start, end = line.split('\t')[1].split()
            entities.add((int(start), int(end), entity_type))
    answers.append(entities)

predictions = [set(entities) for entities in Solution().predict(texts)]

types = sorted({entity[2] for entities in answers for entity in entities})
scores = []
for entity_type in types:
    tp = fp = fn = 0
    for predicted, expected in zip(predictions, answers):
        pred = {e for e in predicted if e[2] == entity_type}
        true = {e for e in expected if e[2] == entity_type}
        tp += len(pred & true)
        fp += len(pred - true)
        fn += len(true - pred)

    f1 = 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else 0
    scores.append(f1)
    print(f'{entity_type:20} F1 = {f1:.4f}')

print(f'\nПроверено текстов: {len(texts)}')
print(f'Средняя F1 по типам: {sum(scores) / len(scores):.4f}')