# Вы можете расположить сценарий своей игры в этом файле.

# Инициализируем Python переменные
init python:

    # Загружаем файл с данными игры
    import copy
    import json
    with renpy.open_file('data.json', encoding='utf-8') as f:
        data_on_start = json.load(f)

    # Цвета
    COLOR_GREEN = '#7CFC00'
    COLOR_RED = '#FF0000'
    COLOR_YELLOW = '#FFFF00'

    def get_color(value):
        """  Возвращаем цвет в завимимости от значения силы тела/духа """
        if value <= 30:
            return COLOR_RED
        elif value < 70:
            return COLOR_YELLOW
        else:
            return COLOR_RED

# Инициализируем данные
init:
    image bg bg = 'bg.jpeg'  # https://www.artstation.com/artwork/1X1r8

# Задаём переменные
default data = copy.deepcopy(data_on_start)
default day = 1
default health = 50
default spirit = 50

# Экран количества дней
screen screen_day():
    text 'День: {color=#7CFC00}[day]{/color}/10':
        xalign 0.02 yalign 0.02

# Экран бодрости тела
screen screen_body():

    $ color = get_color(health)
    text 'Бодрость тела: {color=[color]}[health]{/color}/100':
        xalign 0.20 yalign 0.02


# Экран бодрости духа
screen screen_spirit():
    if spirit >= 50:
        text 'Бодрость духа: {color=#FFFF00}[spirit]{/color}/100':
            xalign 0.50 yalign 0.02
    else:
        text 'Бодрость духа: {color=#FF0000}[spirit]{/color}/100':
            xalign 0.50 yalign 0.02

# Игра начинается здесь:
label start:

    # 1. Показываем фон
    scene bg bg

    # 2. Показываем состояние игрока
    show screen screen_day
    show screen screen_body
    show screen screen_spirit

    # Выводим на экран описание дня
    $ day_description = data['days'][day-1]['description']
    '[day_description]'

    # Если в этот день есть специальное событие, отображаем его
    # Если специального события нет, выбираем событие из пула случайных событий
    $ actions = data['days'][day-1].get('actions')
    if actions:
        pass
    else:
        # Перемешиваем варианты действий, чтобы они были случайными
        $ renpy.random.shuffle(data['actions'])

        # Выбираем событие из пула случайных событий
        $ actions = data['actions']

    # Выбираем варианты действий
    $ text0 = actions[0]['input_text']
    $ text1 = actions[1]['input_text']
    $ text2 = actions[2]['input_text']
    menu:

        '[text0]':
            $ action = actions      [0]

        '[text1]':
            $ action = actions[1]

        '[text2]':
            $ action = actions[2]

# Если у выполненного действия было дочернее действие, добавляем дочернее действие в пул всех действий
if action.get('child'):
    $ data['actions'].append(action['child'])

# Удаляем выполненное действие из общего пула действий
if not data['days'][day-1].get('actions'):
    $ data['actions'].remove(action)

# Выводим на экран результат операции
$ text = action['output_text']
'[text]'

# Выводим на экран изменения в бодрости тела
$ stat_change = ''
if action.get('health'):
    if action['health'] < 0:
        $ color = '{color=' + COLOR_RED + '}'
    else:
        $ color = '{color=' + COLOR_GREEN + '}+'
    $ stat_change += f'Бодрость тела: {color}{action["health"]}' + '{/color}. '

# Выводим на экран изменения в бодрости духа
if action.get('spirit'):
    if action['spirit'] < 0:
        $ color = '{color=' + COLOR_RED + '}'
    else:
        $ color = '{color=' + COLOR_GREEN + '}+'
    $ stat_change += f'Бодрость духа: {color}{action["spirit"]}' + '{/color}. '

# Меняем статы игрока, сообщаем ему об этом
'[stat_change]'
if health + action['health'] < 0:
    $ health = 0
else:
    $ health += action['health']

if spirit + action['spirit'] < 0:
    $ spirit = 0
else:
    $ spirit += action['spirit']

# Если статы игрока упали до нуля, конец игры
if health < 1 or spirit < 1:

    # Составляем текст прощального сообщения
    $ days_left = 10 - day
    $ text = ''
    if days_left == 1:
        $ text = 'оставался всего один день'
    if days_left == 2:
        $ text = 'оставалось всего два дня'
    if days_left == 3:
        $ text = 'оставалось всего три дня'
    if days_left == 4:
        $ text = 'оставалось всего четыре дня'
    if days_left == 5:
        $ text = 'оставалось всего пять дней'
    if days_left == 6:
        $ text = 'оставалось всего шесть дней'


    menu:
        'Мне [text]. Увы, силы покинули меня...':
            return

# Прибавляем новый день
$ day += 1

# Возвращаемся к началу нового дня
jump start