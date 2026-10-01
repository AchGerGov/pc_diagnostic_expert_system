# smart_search.py
from nlp_processor import tokenize


def search_knowledge(query, qa_pairs, top_n=3, min_score=0.15):
    """
    Умный поиск по базе Q&A.
    Возвращает список кортежей (qa, score) — от самых релевантных к менее.
    """
    if not query.strip():
        return []

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return []

    scored = []
    query_lower = query.lower()

    for qa in qa_pairs:
        # Собираем все токены (из вопроса и ключевых слов)
        all_tokens = set(tokenize(qa["question"]))
        for kw in qa.get("keywords", []):
            all_tokens.update(tokenize(kw))

        overlap = query_tokens & all_tokens
        if not overlap:
            continue

        # Базовый скор: доля совпавших слов от запроса
        score = len(overlap) / len(query_tokens)

        # Бонус за точное вхождение ключевой фразы
        for kw in qa.get("keywords", []):
            if kw.lower() in query_lower:
                score += 0.4

        scored.append((score, qa))

    # Сортируем по убыванию
    scored.sort(key=lambda x: x[0], reverse=True)

    # Возвращаем только релевантные
    return [(qa, round(score, 2)) for score, qa in scored[:top_n] if score >= min_score]
