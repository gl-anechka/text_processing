from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
import pickle
import random

from features import tokenize, make_examples

#random.seed(42)

# загрузка данных (из обучающего набора были удалены все разрывные сущности
# по соглашению об условии задания)
texts = []
answers = []
train_dir = Path(__file__).parent / 'NEREL-v1.1' / 'train'

for file in sorted(train_dir.glob('*.txt')):
    texts.append(file.read_text(encoding='utf-8'))
    entities = set()
    for line in file.with_suffix('.ann').read_text(encoding='utf-8').splitlines():
        if line.startswith('T'):
            entity_type, start, end = line.split('\t')[1].split()
            entities.add((int(start), int(end), entity_type))
    answers.append(entities)

# токенизация текста
tokenized_texts = [tokenize(text) for text in texts]

# формирование обучающей выборки
X = []
y = []
for text, tokens, entities in zip(texts, tokenized_texts, answers):
    examples = make_examples(text, tokens, entities)
    for start, end, features, entity_types in examples:
        # уменьшить количество ложных примеров
        #if not entity_types and random.random() > 0.15:
        #    continue
        X.append(features)
        y.append(sorted(entity_types)[0] if entity_types else "NONE")

# преобразование признаков в числовые векторы
vectorizer = DictVectorizer(sparse=True)
X_matrix = vectorizer.fit_transform(X)

# задаём веса обучающих примеров
weights = [40.0 if label != 'NONE' else 1.0 for label in y]

# обучение классификатора
#model = SGDClassifier(loss='log_loss', class_weight='balanced', random_state=42, max_iter=8, tol=None, n_jobs=-1)
model = LinearSVC(C=0.1, random_state=42)
model.fit(X_matrix, y, sample_weight=weights)

# сохранение модели
model_path = Path(__file__).parent / 'model.pkl'
with open(model_path, 'wb') as file:
    pickle.dump((vectorizer, model), file)
print('Модель сохранена')