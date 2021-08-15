from string import punctuation, whitespace, ascii_lowercase


def clean_sentence(sentence: str) -> str:
    words = list(map(clean_word, sentence.split()))
    return " ".join(words)


def clean_word(word):
    return word.translate(clean_word.table).lower()


clean_word.table = {ord(c): "" for c in whitespace + punctuation}


def get_all_suffix(sentence):
    n = len(sentence)
    for i in range(n):
        if n - i > 25:
            yield sentence[i:i + 25]
        else:
            yield sentence[i:]


def all_deletions(sentence):
    for i in range(len(sentence) - 1, -1, -1):
        yield sentence[:i] + sentence[i + 1:], i


def all_replacements(sentence):
    for i in range(len(sentence) - 1, -1, -1):
        for char in ascii_lowercase:
            if char != sentence[i]:
                yield sentence[:i] + char + sentence[i + 1:], i


def all_additions(sentence):
    for i in range(len(sentence) - 1, -1, -1):
        for char in ascii_lowercase:
            yield sentence[:i] + char + sentence[i:], i
