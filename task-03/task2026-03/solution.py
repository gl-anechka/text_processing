from typing import List, Iterable, Set, Tuple
import pickle
from pathlib import Path

# функции обработки данных из обучения модели
from features import tokenize, make_examples

class Solution:
    def __init__(self):
        # загрузка обученной модели
        model_path = Path(__file__).parent / 'model.pkl'
        with open(model_path, 'rb') as file:
            self.vectorizer, self.model = pickle.load(file)

    def predict(self, texts: List[str]) -> Iterable[Set[Tuple[int, int, str]]]:
        results = []

        for text in texts:
            tokens = tokenize(text)
            examples = make_examples(text, tokens, set())
            if not examples:
                results.append(set())
                continue

            X = [features for start, end, features, entity_types in examples]
            X_matrix = self.vectorizer.transform(X)

            scores = self.model.decision_function(X_matrix)
            predictions = self.model.classes_[scores.argmax(axis=1)]

            entities = set()
            for (start, end, features, entity_types), predicted_type in zip(examples, predictions):
                if predicted_type != 'NONE':
                    entities.add((start, end, predicted_type))

            results.append(entities)

        return results