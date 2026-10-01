# nlp_processor.py
# Версия без pymorphy2 — работает на любом Python 3.8+ без внешних зависимостей.
import re

# Набор русских окончаний, которые нужно отсекать (упрощённый стеммер).
# Чем длиннее окончание в начале списка, тем точнее "корень" слова.
ENDINGS = [
    "иями", "ями", "ами", "ией", "иях", "ях", "ах", "ов", "ев", "ий", "ый", "ой",
    "ая", "ое", "ые", "ие", "ую", "юю", "ешь", "ишь", "ете", "ите", "ут", "ют",
    "ат", "ят", "ла", "ло", "ли", "ть", "ся", "сь", "ий", "яя", "ее", "ие",
    "а", "я", "о", "е", "у", "ю", "ы", "и", "ь"
]

def stem(word):
    """
    Упрощённый стеммер: убирает наиболее частые русские окончания.
    Для коротких слов окончания не отсекаются.
    """
    if len(word) <= 3:
        return word
    for end in ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            return word[:-len(end)]
    return word

def tokenize(text):
    """
    Разбивает текст на нормализованные слова (стемы).
    Удаляет знаки препинания, приводит к нижнему регистру.
    """
    words = re.findall(r'[а-яёa-z0-9]+', text.lower(), re.IGNORECASE)
    return [stem(w) for w in words if len(w) > 2]

def match_symptoms(text, available_symptoms):
    """
    Сопоставляет текст пользователя со списком симптомов.
    Возвращает список симптомов, в которых найдено хотя бы одно общее слово.
    """
    if not text or not text.strip():
        return []

    user_stems = set(tokenize(text))
    matched = []

    for symptom in available_symptoms:
        symptom_stems = set(tokenize(symptom))
        if user_stems.intersection(symptom_stems):
            matched.append(symptom)

    return matched
