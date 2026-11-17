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
    features = {'first': first.lower(),  # первое слово сущности
            'last': last.lower(),  # последнее слово сущности
            'length': len(words),  # длина фрагмента

            'first_upper': first[0].isupper(),  # заглавная буква
            'last_upper': last[0].isupper(),  # заглавная буква

            'has_digit': any(c.isdigit() for c in fragment),  # наличие цифр
            'has_hyphen': '-' in fragment,  # для составных названий

            'previous': tokens[i - 1][0].lower() if i > 0 else '',  # контекст
            'next': tokens[j + 1][0].lower() if j + 1 < len(tokens) else '',  # контекст

            'first_suffix2': first.lower()[-2:],  # окончание первого слова
            'first_suffix3': first.lower()[-3:],  # окончание первого слова
            'last_suffix2': last.lower()[-2:],  # окончание последнего слова
            'last_suffix3': last.lower()[-3:],  # окончание последнего слова

            'all_capitalized': all(w[0].isupper() for w in words),  # фрагменты из слов с заглавной буквы
            'n_capitalized': min(5, sum(w[0].isupper() for w in words))}  # кол-во таких слов

    # наличие слов внутри фрагмента
    for word in words:
        features['inside_word=' + word.lower()] = True

    return features


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