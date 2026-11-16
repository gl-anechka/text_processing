import re

# функция, разбивающая текст на токены (по словам)
def tokenize(text):
    tokens = []
    for match in re.finditer(r'\w+|[^\w\s]', text):
        tokens.append((match.group(), match.start(), match.end()))
    return tokens


# функция выделения признаков фрагмента
def extract_features(text, tokens, i, j):
    words = [token[0] for token in tokens[i:j+1]]
    first = words[0]
    last = words[-1]
    start = tokens[i][1]
    end = tokens[j][2]
    fragment = text[start:end]
    return {'first': first.lower(),
            'last': last.lower(),
            'length': len(words),
            'first_upper': first[0].isupper(),
            'last_upper': last[0].isupper(),
            'has_digit': any(c.isdigit() for c in fragment),
            'has_hyphen': '-' in fragment,
            'previous': tokens[i - 1][0].lower() if i > 0 else ''}


# функция, которая создает обучающие примеры для модели
# фрагменты длиной не более 10 токенов
def make_examples(text, tokens, entities):
    examples = []
    labels = {}  # словарь, ключ - границы сущности, значение - множество типов
    for start, end, entity_type in entities:
        labels.setdefault((start, end), set()).add(entity_type)

    for i in range(len(tokens)):  # индекс первого токена
        for j in range(i, min(i + 10, len(tokens))):  # индекс последнего токена
            start = tokens[i][1]
            end = tokens[j][2]
            features = extract_features(text, tokens, i, j)
            entity_types = labels.get((start, end), set())
            examples.append((start, end, features, entity_types))
    return examples