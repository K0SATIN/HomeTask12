import json
from pathlib import Path

pages = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для присваивания значения?',
        'options': ['=', 'is', 'assuming', '^'],
        'correct_option': 0
    },
    {
        'question': 'Библиотекой для построения графиков является....',
        'options': ['seaborn', 'json', 'pandas', 'numpy '],
        'correct_option': 0
    },
    {
        'question': 'Однострочные комментарии в python выделяются знаком....',
        'options': ['#', '//', '!', '+++'],
        'correct_option': 0
    },
    {
        'question': 'Способ отмечать тело цикла в python - ',
        'options': ['отступ слева', 'пара begin-end', 'фигурные скобки', 'тройные кавычки'],
        'correct_option': 0
    },
    {
        'question': 'Для чего используются квадратные скобки?',
        'options': ['Для обозначения массивов', 'Для обозначения списков', 'Для обозначения аргументов функции', 'Это знак присваивания'],
        'correct_option': 0
    },
    {
        'question': 'Ключевое слово def используется для чего?',
        'options': ['Обозначение функции', 'Объявление переменной', 'В паре с end для обозначения тела цикла', 'Для импорта библиотек'],
        'correct_option': 0
    },
    {
        'question': 'Для инкремента переменной some_val используется.....',
        'options': ['some_val += 1', 'some_val++', 'increment(some_val)', 'some_val(+1)'],
        'correct_option': 0
    },
    {
        'question': 'На сколько вопросов вы уже дали ответ(не считая этот?)',
        'options': ['9', '10', '11', '8'],
        'correct_option': 0
    }
    # Добавьте другие вопросы
]
path = Path('pages.json')
path.write_text(json.dumps(pages, indent=2), encoding='utf-8')  # write