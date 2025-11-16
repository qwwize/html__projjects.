Общайтесь с командой и задавайте вопросы о GitVerse в нашем чате в Telegram
Close
/
urfu_itis_tasks_alt
/
vibe_coding_101-yanasim
Обзор

2

Поиск
/

Аватар пользователя
Код
Запросы
1
Задачи
Вики
Пакеты
0
Релизы
0
CI/CD
Аналитика
New
Безопасность
Настройки

vibe_coding_101-yanasim
 Форк из urfu_itis_tasks_alt/vibe_template-snapshot-WzUQf

Не следить
Форк
0

Избранное
0
GigaIDE Cloud


feature-yanasim

Ветки:
2
Коммиты:
6
Теги:
0

Файл

Код
vibe_coding_101-yanasim
/assignment.py 
229 строк · 6,6 Кб
О чем код?
Raw



Перенос по строкам
"""
Анализ датасета BoolQ (Boolean Questions).

Модуль для анализа распределения да/нет ответов в датасете BoolQ,
статистики длин текстов и характеристических слов для каждого класса.
"""

import json
import re
from collections import Counter
from typing import Dict, List, Any

import numpy as np
from datasets import load_dataset
import matplotlib.pyplot as plt


def load_boolq_dataset(sample_size: int = 1000) -> List[Dict[str, Any]]:
    """
    Загружает датасет BoolQ из Hugging Face.

    Args:
        sample_size: Количество примеров для загрузки.

    Returns:
        Список словарей с полями question, passage, answer.

    Examples:
        >>> data = load_boolq_dataset(100)
        >>> len(data) <= 100
        True
    """
    dataset = load_dataset("google/boolq", split="train")
    return [dataset[i] for i in range(min(sample_size, len(dataset)))]


def preprocess_text(text: str) -> List[str]:
    """
    Предобработка текста: lowercase и удаление спецсимволов.

    Args:
        text: Исходный текст.

    Returns:
        Список слов в нижнем регистре.

    Examples:
        >>> preprocess_text("Hello, World!")
        ['hello', 'world']
    """
    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)
    return words


def analyze_answer_distribution(dataset: List[Dict]) -> Dict[str, Any]:
    """
    Анализирует распределение true/false ответов.

    Args:
        dataset: Список примеров BoolQ.

    Returns:
        Dict с ключами: true_count, false_count, true_percent, false_percent.

    Examples:
        >>> data = [{"answer": True}, {"answer": False}]
        >>> result = analyze_answer_distribution(data)
        >>> result["true_count"]
        1
    """
    answers = [item["answer"] for item in dataset]
    true_count = sum(answers)
    false_count = len(answers) - true_count

    return {
        "total": len(answers),
        "true_count": true_count,
        "false_count": false_count,
        "true_percent": round(100 * true_count / len(answers), 2),
        "false_percent": round(100 * false_count / len(answers), 2)
    }


def analyze_text_lengths(dataset: List[Dict]) -> Dict[str, Dict[str, float]]:
    """
    Вычисляет статистику длин вопросов и контекстов.

    Args:
        dataset: Список примеров BoolQ.

    Returns:
        Dict со статистикой для questions и passages.

    Examples:
        >>> data = [{"question": "Is it?", "passage": "Yes"}]
        >>> result = analyze_text_lengths(data)
        >>> "questions" in result
        True
    """
    q_lens = [len(item["question"]) for item in dataset]
    p_lens = [len(item["passage"]) for item in dataset]

    return {
        "questions": {
            "mean": round(np.mean(q_lens), 2),
            "median": round(np.median(q_lens), 2),
            "min": int(np.min(q_lens)),
            "max": int(np.max(q_lens))
        },
        "passages": {
            "mean": round(np.mean(p_lens), 2),
            "median": round(np.median(p_lens), 2),
            "min": int(np.min(p_lens)),
            "max": int(np.max(p_lens))
        }
    }


def extract_characteristic_words(
    dataset: List[Dict], top_n: int = 15
) -> Dict[str, List[tuple]]:
    """
    Извлекает топ слов отдельно для true и false ответов.

    Args:
        dataset: Список примеров BoolQ.
        top_n: Количество топ слов.

    Returns:
        Dict с ключами true_words и false_words.

    Examples:
        >>> data = [{"question": "Is good?", "answer": True}]
        >>> result = extract_characteristic_words(data, 1)
        >>> len(result["true_words"]) >= 0
        True
    """
    true_words = []
    false_words = []

    for item in dataset:
        words = preprocess_text(item["question"])
        if item["answer"]:
            true_words.extend(words)
        else:
            false_words.extend(words)

    true_counter = Counter(true_words).most_common(top_n)
    false_counter = Counter(false_words).most_common(top_n)

    return {
        "true_words": true_counter,
        "false_words": false_counter
    }


def create_visualization(dataset: List[Dict]) -> None:
    """
    Создает bar chart распределения true/false и сохраняет в PNG.

    Args:
        dataset: Список примеров BoolQ.

    Returns:
        None. Сохраняет файл visualization.png.
    """
    dist = analyze_answer_distribution(dataset)

    fig, ax = plt.subplots(figsize=(8, 6))
    categories = ['True', 'False']
    counts = [dist['true_count'], dist['false_count']]
    colors = ['#2ecc71', '#e74c3c']

    ax.bar(categories, counts, color=colors, alpha=0.8)
    ax.set_xlabel('Answer Type', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('BoolQ Answer Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    for i, (cat, count) in enumerate(zip(categories, counts)):
        ax.text(i, count + 10, str(count), ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig('visualization.png', dpi=150)
    plt.close()


def main() -> None:
    """
    Основная функция: загружает данные, анализирует и сохраняет результаты.
    """
    print("Loading BoolQ dataset...")
    dataset = load_boolq_dataset(1000)

    print("Analyzing answer distribution...")
    dist = analyze_answer_distribution(dataset)

    print("Analyzing text lengths...")
    lengths = analyze_text_lengths(dataset)

    print("Extracting characteristic words...")
    words = extract_characteristic_words(dataset, 15)

    print("Creating visualization...")
    create_visualization(dataset)

    # Сохранение результатов в JSON
    results = {
        "dataset": "google/boolq",
        "sample_size": len(dataset),
        "answer_distribution": dist,
        "text_statistics": lengths,
        "characteristic_words": {
            "true_words": dict(words["true_words"][:10]),
            "false_words": dict(words["false_words"][:10])
        }
    }

    with open('boolq_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("[OK] Analysis complete! Files saved:")
    print("  - boolq_results.json")
    print("  - visualization.png")


if __name__ == "__main__":
    main()

Документация
Поддержка
Оценить
Политика конфиденциальности
Пользовательское соглашение
Политика использования «cookies»
Согласие субъекта персональных данных
2025 ©
assignment.py - feature-yanasim - urfu_itis_tasks_alt/vibe_coding_101-yanasim - Gitverse
